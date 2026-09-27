#!/usr/bin/env python3
"""Read-only source availability/change receipts and a dated editorial review queue.

An HTTP success never promotes a record. Bot blocks are reported separately from
missing pages. Hash changes request review; they do not establish a legal change.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

CONTENT = Path(__file__).resolve().parents[1] / 'content' / 'compliance-directory'


def check(source, timeout):
    result = {'id': source['id'], 'url': source['url']}
    try:
        request = urllib.request.Request(source['url'], headers={'User-Agent': 'QuickTrust-directory-source-check/1.0'})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_000)
            result.update(status=response.status, finalUrl=response.url, sha256=hashlib.sha256(body).hexdigest(), result='reachable')
    except urllib.error.HTTPError as error:
        result.update(status=error.code, result='blocked-or-rate-limited' if error.code in (401, 403, 429) else 'needs-review')
    except Exception as error:
        result.update(status=None, result='unavailable', error=type(error).__name__)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--timeout', type=int, default=20)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Choose a new output path; preserve earlier receipts.')
    sources = json.loads((CONTENT / 'sources.json').read_text())
    records = json.loads((CONTENT / 'requirements.json').read_text())
    previous = {s['id']: s for s in json.loads(args.previous.read_text())['sources']} if args.previous else {}
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as executor:
        checks = list(executor.map(lambda s: check(s, args.timeout), sources))
    for item in checks:
        before = previous.get(item['id'], {})
        item['contentChanged'] = bool(item.get('sha256') and before.get('sha256') and item['sha256'] != before['sha256'])
    review_ids = {s['id'] for s in checks if s['result'] != 'reachable' or s['contentChanged']}
    horizon = (date.today() + timedelta(days=7)).isoformat()
    queue = [{'id': r['id'], 'status': r['status'], 'nextReviewAt': r['nextReviewAt'], 'reasons': [reason for condition, reason in [
        (r['status'] == 'draft', 'Complete authority, applicability, current-status and substantive content review'),
        (r['nextReviewAt'] <= horizon, 'Scheduled review due within seven days'),
        (bool(set(r['sourceIds']) & review_ids), 'Source availability or content-change review required')
    ] if condition]} for r in records]
    queue = [r for r in queue if r['reasons']]
    report = {'checkedAt': date.today().isoformat(), 'method': 'Availability and bounded response hash only. HTML template changes can alter hashes. No automatic legal conclusions or publication changes.', 'sources': checks, 'reviewQueue': queue}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'sources': len(checks), 'reachable': sum(c['result'] == 'reachable' for c in checks), 'needsReview': len(review_ids), 'editorialQueue': len(queue), 'report': str(args.output)}))


if __name__ == '__main__':
    main()
