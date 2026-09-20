"""Deploy only the existing verified QuickTrust frontend; never alter app settings."""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UUID = 'e92mp4jy5j3nojkgsyqhqbwd'
HOST = 'https://infra.quickintell.com/api/v1'
REPO = 'allgpt-co/quicktrustfinal'


def request(url, token, body=None):
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'User-Agent': 'QuickTrust-Frontend-Release/1.0'}
    payload = None
    if body is not None:
        payload = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=payload, headers=headers), timeout=40) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'API refused request with HTTP {error.code}; no permission or settings changes attempted') from None
    except (urllib.error.URLError, ValueError, TimeoutError):
        raise RuntimeError('API request failed; recheck deployment state before retrying a write') from None


def valid_app(app):
    domains = {urllib.parse.urlsplit(value.strip()).hostname for value in app.get('fqdn', '').split(',')}
    repository = app.get('git_repository', '').removesuffix('.git').removeprefix('https://github.com/')
    return app.get('uuid') == UUID and 'quicktrustapp.com' in domains and repository == REPO and app.get('git_branch') == 'main' and app.get('base_directory') == '/frontend'


def main():
    commit = os.environ['EXPECTED_COMMIT']
    if not re.fullmatch('[0-9a-f]{40}', commit) or commit != os.environ['GITHUB_SHA']:
        raise RuntimeError('Requested release does not match the workflow commit')
    token = os.environ['COOLIFY_API_TOKEN']
    gh_token = os.environ['GH_TOKEN']
    git_api = 'https://api.github.com/repos/' + REPO
    head = request(git_api + '/git/ref/heads/main', gh_token)['object']['sha']
    if head != commit:
        raise RuntimeError('Main changed; validate the new revision before deploying')
    checks = request(git_api + '/commits/' + commit + '/check-runs', gh_token)['check_runs']
    if not any(item.get('name') == 'Trivy filesystem scan' and item.get('conclusion') == 'success' for item in checks):
        raise RuntimeError('Current main lacks a successful security check')
    app = request(HOST + '/applications/' + UUID, token)
    if not valid_app(app):
        raise RuntimeError('Existing application identity does not match the approved frontend')
    print(json.dumps({'verified_app': UUID, 'domain': 'quicktrustapp.com', 'branch': 'main', 'base_directory': '/frontend', 'expected_commit': commit}))
    if os.environ.get('APPLY_DEPLOY') != 'true':
        print('Read-only preflight passed; no deployment requested')
        return
    # A single request only. An uncertain response is never automatically retried.
    result = request(HOST + '/deploy', token, {'uuid': UUID, 'force': False})
    rows = [item for item in result.get('deployments', []) if item.get('resource_uuid') == UUID]
    if len(rows) != 1 or not re.fullmatch('[A-Za-z0-9_-]+', rows[0].get('deployment_uuid', '')):
        raise RuntimeError('Deployment receipt uncertain; inspect current state before retrying')
    deployment = rows[0]['deployment_uuid']
    print(json.dumps({'deployment_uuid': deployment, 'status': 'queued'}), flush=True)
    for _ in range(40):
        time.sleep(30)
        state = request(HOST + '/deployments/' + deployment, token)
        status = state.get('status')
        if status == 'finished':
            if state.get('commit') != commit:
                raise RuntimeError('Deployment finished with an unexpected commit; public acceptance withheld')
            print(json.dumps({'deployment_uuid': deployment, 'status': status, 'commit': commit}))
            return
        if status in ('failed', 'cancelled', 'canceled'):
            raise RuntimeError('Deployment reached ' + status)
    raise RuntimeError('Deployment still pending; inspect state before retrying')


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
