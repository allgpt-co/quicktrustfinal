"""HTTP release gate for public marketing aliases, downloads, sitemap and auth."""
import argparse
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'QuickTrust-Release-Check/1.0'})
    try:
        response = urllib.request.build_opener(NoRedirect).open(request, timeout=30)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, dict(response.headers), response.read().decode('utf-8', errors='replace')


def header(headers, name):
    return next((value for key, value in headers.items() if key.lower() == name), '')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='https://quicktrustapp.com')
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--observe', action='store_true', help='Record failures without failing the baseline run')
    args = parser.parse_args()
    if args.report.exists():
        raise SystemExit('Use a fresh report path; never overwrite a prior acceptance receipt')
    base = args.base.rstrip('/')
    root = Path(__file__).resolve().parents[1]
    aliases = json.loads((root / 'src/lib/marketing-content-redirects.json').read_text())
    resources = ['soc2-readiness-scorecard', 'iso27001-gap-assessment-checklist', 'hipaa-risk-assessment-template', 'audit-evidence-checklist', '15-security-policy-templates']
    checks = []
    def check_alias(item):
        source, target = item
        status, headers, _ = fetch(base + source)
        destination = urllib.parse.urlsplit(header(headers, 'location')).path
        return {'path': source, 'status': status, 'destination': destination, 'expected': target, 'ok': status in (301, 308) and destination == target}
    def check_target(target):
        status, _, html = fetch(base + target)
        expected = 'https://quicktrustapp.com' + target
        return {'path': target, 'status': status, 'ok': status == 200 and ('rel="canonical" href="' + expected + '"') in html}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checks.extend(pool.map(check_alias, aliases.items()))
        checks.extend(pool.map(check_target, sorted(set(aliases.values()))))
    for slug in resources:
        path = '/resources/' + slug
        status, headers, content = fetch(base + path)
        checks.append({'path': path, 'status': status, 'ok': status == 200 and 'attachment' in header(headers, 'content-disposition') and 'text/markdown' in header(headers, 'content-type') and header(headers, 'x-robots-tag') == 'noindex' and len(content) > 1000})
    for path in ['/dashboard', '/settings', '/resources/private', '/content/private']:
        status, headers, _ = fetch(base + path)
        checks.append({'path': path, 'status': status, 'ok': status == 307 and urllib.parse.urlsplit(header(headers, 'location')).path == '/login'})
    status, _, xml = fetch(base + '/sitemap.xml')
    sitemap_ok, url_count = False, 0
    if status == 200:
        document = ET.fromstring(xml)
        urls = document.findall('{*}url')
        url_count = len(urls)
        sitemap_ok = True
        for entry in urls:
            location = entry.findtext('{*}loc', '')
            path = urllib.parse.urlsplit(location).path
            modified = entry.findtext('{*}lastmod')
            if path in aliases or path.startswith('/resources/') or (not path.startswith('/blog/') and modified):
                sitemap_ok = False
    checks.append({'path': '/sitemap.xml', 'status': status, 'urls': url_count, 'ok': sitemap_ok})
    result = {'observed_at': datetime.now(timezone.utc).isoformat(), 'base': base, 'checks': checks, 'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'checks'}))
    if result['failed'] and not args.observe:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
