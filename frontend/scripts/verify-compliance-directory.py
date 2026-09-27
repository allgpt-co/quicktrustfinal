#!/usr/bin/env python3
"""Read-only HTTP acceptance against a built local or deployed marketing site."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import gzip
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'content' / 'compliance-directory'
PREFIX = '/compliance-directory'
ORIGIN = 'https://quicktrustapp.com'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


class Head(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1 = 0; self.titles = 0; self.canonicals = []; self.robots = []; self.description = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.h1 += tag == 'h1'; self.titles += tag == 'title'
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonicals.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('name') == 'robots': self.robots.append(attrs.get('content', ''))
        if tag == 'meta' and attrs.get('name') == 'description': self.description.append(attrs.get('content', ''))


def fetch(base, path):
    opener = urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(base + path, headers={'User-Agent': 'QuickTrust-directory-acceptance/1.0', 'Accept-Encoding': 'gzip'})
    try:
        response = opener.open(request, timeout=45)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        body = response.read()
        if response.headers.get('Content-Encoding') == 'gzip': body = gzip.decompress(body)
        return response.status, response.headers, body.decode('utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default=ORIGIN)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    if args.report.exists(): parser.error('Use a fresh report path')
    requirements = json.loads((ROOT / 'requirements.json').read_text())
    geography = json.loads((ROOT / 'geography.json').read_text()) + json.loads((ROOT / 'jurisdictions-extra.json').read_text())
    industries = json.loads((ROOT / 'industries.json').read_text())
    checks = []
    cases = [(PREFIX, False), (PREFIX + '/coverage', False)]
    cases += [(PREFIX + '/' + route, True) for route in ['countries', 'industries', 'sources', 'updates', 'finder', 'finder?location=US&activity=I', 'finder?q=unrecorded-no-match', 'compare', 'compare?id=iso-9001&id=cyber-essentials']]
    cases += [(PREFIX + '/jurisdictions/' + j['id'].lower(), True) for j in geography if j['kind'] != 'subdivision']
    # All countries plus one subdivision for every country that has one.
    seen = set()
    for j in geography:
        country = j['id'].split('-')[0]
        if j['kind'] == 'subdivision' and country not in seen:
            cases.append((PREFIX + '/jurisdictions/' + j['id'].lower(), True)); seen.add(country)
    cases += [(PREFIX + '/industries/' + i['id'].lower(), True) for i in industries]
    for r in requirements:
        if r['canonicalPath'].startswith(PREFIX + '/'):
            verified = r['status'] == 'verified' and r['nextReviewAt'] >= date.today().isoformat()
            cases.append((r['canonicalPath'], not verified))

    def verify(case):
        path, noindex = case
        try:
            status, headers, body = fetch(args.base.rstrip('/'), path)
            head = Head(); head.feed(body)
            errors = []
            if status != 200: errors.append(f'HTTP {status}')
            if head.h1 != 1 or head.titles != 1: errors.append(f'h1={head.h1}, titles={head.titles}')
            if head.canonicals != [ORIGIN + path.split('?')[0]]: errors.append(f'canonical={head.canonicals}')
            if len(head.description) != 1 or not head.description[0]: errors.append('missing/duplicate description')
            if any('noindex' in x for x in head.robots) != noindex: errors.append(f'robots={head.robots}')
            return {'path': path, 'passed': not errors, 'errors': errors}
        except Exception as error:
            return {'path': path, 'passed': False, 'errors': [str(error)]}

    with ThreadPoolExecutor(max_workers=6) as executor: checks.extend(executor.map(verify, cases))
    for r in requirements:
        if not r['canonicalPath'].startswith(PREFIX + '/'):
            status, headers, _ = fetch(args.base.rstrip('/'), PREFIX + '/requirements/' + r['id'])
            checks.append({'path': PREFIX + '/requirements/' + r['id'], 'passed': status == 308 and headers.get('Location') == r['canonicalPath'], 'status': status, 'location': headers.get('Location')})
    for r in requirements:
        expected = 200 if r['status'] == 'verified' and r['nextReviewAt'] >= date.today().isoformat() else 409
        status, headers, body = fetch(args.base.rstrip('/'), PREFIX + '/checklists/' + r['id'])
        passed = status == expected and 'noindex' in headers.get('X-Robots-Tag', '')
        if expected == 200: passed = passed and 'Source: https://' in body and 'Reviewed:' in body and 'attachment;' in headers.get('Content-Disposition', '')
        checks.append({'path': PREFIX + '/checklists/' + r['id'], 'passed': passed, 'status': status})
    expected_urls = {ORIGIN + PREFIX, ORIGIN + PREFIX + '/coverage'} | {ORIGIN + r['canonicalPath'] for r in requirements if r['status'] == 'verified' and r['nextReviewAt'] >= date.today().isoformat() and r['canonicalPath'].startswith(PREFIX + '/')}
    _, _, index = fetch(args.base.rstrip('/'), PREFIX + '/sitemap.xml')
    urls = []
    for node in ET.fromstring(index).findall('.//{*}loc'):
        _, _, shard = fetch(args.base.rstrip('/'), node.text.removeprefix(ORIGIN))
        urls += [n.text for n in ET.fromstring(shard).findall('.//{*}loc')]
    checks.append({'path': PREFIX + '/sitemap.xml', 'passed': set(urls) == expected_urls and len(urls) == len(expected_urls), 'urls': urls})
    for path in ['/frameworks', '/frameworks/iso-9001', '/settings/integrations', '/settings/trust-center']:
        status, headers, _ = fetch(args.base.rstrip('/'), path)
        checks.append({'path': path, 'passed': status == 307 and '/login?' in headers.get('Location', ''), 'status': status})
    for path in [PREFIX + '/requirements/unknown', PREFIX + '/jurisdictions/unknown', PREFIX + '/industries/unknown']:
        status, _, _ = fetch(args.base.rstrip('/'), path)
        checks.append({'path': path, 'passed': status == 404, 'status': status})
    report = {'base': args.base, 'checkedAt': date.today().isoformat(), 'checks': len(checks), 'passed': sum(c['passed'] for c in checks), 'results': checks}
    args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}))
    for failed in [c for c in checks if not c['passed']]: print(json.dumps(failed))
    raise SystemExit(0 if report['passed'] == report['checks'] else 1)


if __name__ == '__main__': main()
