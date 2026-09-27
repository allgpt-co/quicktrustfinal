#!/usr/bin/env python3
"""Refresh reference inventories only. Never promote requirement verification.

Run from any directory; review the resulting diff before committing.
No credentials, application database or runtime network dependencies.
"""
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import urllib.request
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1] / 'content' / 'compliance-directory'
DATE = datetime.now(timezone.utc).date().isoformat()
PYCOUNTRY_COMMIT = '4c6a69927a25326a69bf753671fb571bb437cd7d'


def fetch(url):
    request = urllib.request.Request(quote(url, safe=':/?=&,'), headers={'User-Agent': 'QuickTrust-directory-research/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    receipts = []
    geography = []
    for suffix in ['1', '2']:
        url = f'https://raw.githubusercontent.com/pycountry/pycountry/{PYCOUNTRY_COMMIT}/src/pycountry/databases/iso3166-{suffix}.json'
        raw = fetch(url)
        records = json.loads(raw)[f'3166-{suffix}']
        receipts.append({'dataset': f'ISO 3166-{suffix} codes via Debian/pycountry', 'url': url, 'retrievedAt': DATE, 'sha256': hashlib.sha256(raw).hexdigest(), 'count': len(records), 'verification': 'Upstream snapshot; reconciliation against ISO OBP pending.'})
        for row in records:
            if suffix == '1':
                geography.append({'id': row['alpha_2'], 'name': row.get('common_name', row['name']), 'officialName': row.get('official_name', row['name']), 'kind': 'country', 'parent': None, 'sourceId': 'iso-geography'})
            else:
                country = row['code'].split('-')[0]
                parent = row.get('parent')
                parent_code = parent if parent and parent.startswith(country + '-') else f'{country}-{parent}' if parent else country
                geography.append({'id': row['code'], 'name': row['name'], 'kind': 'subdivision', 'localType': row['type'], 'parent': parent_code, 'sourceId': 'iso-geography'})
    write('geography.json', sorted(geography, key=lambda x: x['id']))

    url = 'https://unstats.un.org/unsd/classifications/Econ/Download/In Text/ISIC_Rev_5_english_structure.csv'
    raw = fetch(url)
    industries = []
    section = None
    # The official CSV currently uses Windows-1252, including non-breaking spaces.
    try:
        decoded = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        decoded = raw.decode('cp1252')
    for row in csv.DictReader(io.StringIO(decoded)):
        code, name = row['ISIC Rev 5 Code'], row['ISIC Rev 5 Title']
        if code.isalpha():
            section = code
        parent = None if code.isalpha() else section if len(code) == 2 else code[:-1]
        industries.append({'id': code, 'name': name, 'parent': parent, 'level': 'section' if code.isalpha() else {2: 'division', 3: 'group', 4: 'class'}[len(code)]})
    write('industries.json', industries)
    receipts.append({'dataset': 'UN ISIC Rev.5 structure', 'url': quote(url, safe=':/'), 'retrievedAt': DATE, 'sha256': hashlib.sha256(raw).hexdigest(), 'count': len(industries), 'verification': 'Full official CSV structure imported; activity-to-requirement mapping is separately reviewed.'})

    url = 'https://www.gov.uk/api/search.json?filter_format=licence_transaction&count=1000&fields=title,link,licence_transaction_location,licence_transaction_industry'
    raw = fetch(url)
    result = json.loads(raw)
    assert len(result['results']) == result['total'], 'Catalogue pagination required; do not silently truncate'
    previous_path = ROOT / 'uk-catalogue.json'
    previous = {r['url']: r for r in json.loads(previous_path.read_text())} if previous_path.exists() else {}
    inventory = []
    for row in result['results']:
        official_url = 'https://www.gov.uk' + row['link']
        decision = previous.get(official_url, {})
        inventory.append({'name': row['title'], 'url': official_url, 'locations': row.get('licence_transaction_location', []), 'activities': row.get('licence_transaction_industry', []), 'status': decision.get('status', 'unreviewed'), 'note': decision.get('note', 'Triage business/professional scope, issuing authority, duplicates and current status before creating a requirement record.')})
    write('uk-catalogue.json', sorted(inventory, key=lambda x: x['name']))
    receipts.append({'dataset': 'GOV.UK Find a licence catalogue', 'url': url, 'retrievedAt': DATE, 'sha256': hashlib.sha256(raw).hexdigest(), 'count': len(inventory), 'verification': 'Complete source catalogue snapshot, not a complete UK obligations list. Includes personal permits pending scope triage.'})
    write('imports.json', receipts)
    for name in ['LICENSE.txt', 'COPYRIGHT.txt']:
        (ROOT / ('pycountry-' + name)).write_bytes(fetch(f'https://raw.githubusercontent.com/pycountry/pycountry/{PYCOUNTRY_COMMIT}/{name}'))
    print(json.dumps({'jurisdictions': len(geography), 'industries': len(industries), 'catalogueLeads': len(inventory)}))


if __name__ == '__main__':
    main()
