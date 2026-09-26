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
from html.parser import HTMLParser


class PageMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.robots = ''
        self.titles = []
        self.in_title = False
        self.h1_count = 0
        self.description = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.robots = attrs.get('content', '')
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content', '')
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'title':
            self.in_title = True
            self.titles.append('')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titles[-1] += data


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
    def check_page(item):
        path, indexable = item
        status, _, html = fetch(base + path)
        page = PageMetadata()
        page.feed(html)
        expected = 'https://quicktrustapp.com' + path
        canonical_ok = len(page.canonical) == 1 and page.canonical[0].rstrip('/') == expected.rstrip('/')
        return {'path': path, 'status': status, 'kind': 'page', 'title': page.titles,
                'ok': status == 200 and canonical_ok and len(page.titles) == 1 and bool(page.titles[0])
                and bool(page.description) and page.h1_count == 1 and (('noindex' not in page.robots) == indexable)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checks.extend(pool.map(check_alias, aliases.items()))
        checks.extend(pool.map(check_target, sorted(set(aliases.values()))))
    for slug in resources:
        path = '/resources/' + slug
        status, headers, content = fetch(base + path)
        checks.append({'path': path, 'status': status, 'ok': status == 200 and 'attachment' in header(headers, 'content-disposition') and 'text/markdown' in header(headers, 'content-type') and header(headers, 'x-robots-tag') == 'noindex' and len(content) > 1000})
    for path in ['/dashboard', '/settings', '/settings/trust-center', '/settings/integrations', '/integrations/123', '/resources/private', '/content/private']:
        status, headers, _ = fetch(base + path)
        checks.append({'path': path, 'status': status, 'ok': status == 307 and urllib.parse.urlsplit(header(headers, 'location')).path == '/login'})
    status, _, xml = fetch(base + '/sitemap.xml')
    sitemap_ok, url_count = False, 0
    sitemap_paths = []
    if status == 200:
        document = ET.fromstring(xml)
        urls = document.findall('{*}url')
        url_count = len(urls)
        sitemap_ok = True
        for entry in urls:
            location = entry.findtext('{*}loc', '')
            path = urllib.parse.urlsplit(location).path
            sitemap_paths.append(path or '/')
            modified = entry.findtext('{*}lastmod')
            if path in aliases or path in ['/resources/' + slug for slug in resources] or (not path.startswith('/blog/') and modified):
                sitemap_ok = False
        if len(set(sitemap_paths)) != url_count:
            sitemap_ok = False
    checks.append({'path': '/sitemap.xml', 'status': status, 'urls': url_count, 'ok': sitemap_ok})
    # Canonical pages, not just redirect targets, must be crawlable and indexable.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checks.extend(pool.map(check_page, [(path, True) for path in sitemap_paths]))
    # Publication records also cover intentional noindex pages and all four hubs.
    for filename in sorted((root / 'content/marketing-pages').glob('*.md')):
        fields = dict(line.split(': ', 1) for line in filename.read_text().split('---', 2)[1].splitlines()
                      if line and not line.startswith(' ') and ': ' in line)
        path = json.loads(fields['path'])
        indexable = fields['indexable'] == 'true'
        checks.append({'path': path, 'kind': 'sitemap-membership', 'ok': (path in sitemap_paths) == indexable})
        if not indexable:
            checks.append(check_page((path, False)))
    for path in ['/privacy-policy', '/terms-of-service']:
        checks.append({'path': path, 'kind': 'noindex-excluded', 'ok': path not in sitemap_paths})
        checks.append(check_page((path, False)))
    result = {'observed_at': datetime.now(timezone.utc).isoformat(), 'base': base, 'checks': checks, 'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'checks'}))
    if result['failed'] and not args.observe:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
