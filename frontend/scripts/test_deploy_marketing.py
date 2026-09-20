import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deploy', Path(__file__).with_name('deploy-marketing.py'))
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)
SHA = 'a' * 40
APP = {'uuid': deploy.UUID, 'fqdn': 'https://quicktrustapp.com,https://www.quicktrustapp.com', 'git_repository': deploy.REPO, 'git_branch': 'main', 'base_directory': '/frontend'}
ENV = {'EXPECTED_COMMIT': SHA, 'GITHUB_SHA': SHA, 'COOLIFY_API_TOKEN': 'test', 'GH_TOKEN': 'test', 'APPLY_DEPLOY': 'false'}
CHECKS = {'check_runs': [{'name': 'Trivy filesystem scan', 'conclusion': 'success'}]}


class DeploymentGuards(unittest.TestCase):
    def test_identity_rejects_other_repo_branch_path_domain(self):
        self.assertTrue(deploy.valid_app(APP))
        for key, value in [('uuid', 'other'), ('fqdn', 'https://other.example'), ('git_repository', 'other/repo'), ('git_branch', 'dev'), ('base_directory', '/backend')]:
            self.assertFalse(deploy.valid_app({**APP, key: value}))

    def test_readonly_preflight_never_deploys(self):
        with patch.dict(os.environ, ENV), patch.object(deploy, 'request', side_effect=[{'object': {'sha': SHA}}, CHECKS, APP]) as api:
            deploy.main()
            self.assertEqual(api.call_count, 3)
            self.assertTrue(all(len(call.args) == 2 for call in api.call_args_list))

    def test_changed_head_stops_before_coolify(self):
        with patch.dict(os.environ, ENV), patch.object(deploy, 'request', return_value={'object': {'sha': 'b' * 40}}) as api:
            with self.assertRaisesRegex(RuntimeError, 'Main changed'):
                deploy.main()
            self.assertEqual(api.call_count, 1)

    def test_uncertain_deployment_is_not_retried(self):
        with patch.dict(os.environ, {**ENV, 'APPLY_DEPLOY': 'true'}), patch.object(deploy, 'request', side_effect=[{'object': {'sha': SHA}}, CHECKS, APP, {}]) as api:
            with self.assertRaisesRegex(RuntimeError, 'receipt uncertain'):
                deploy.main()
            self.assertEqual(api.call_count, 4)


if __name__ == '__main__':
    unittest.main()
