from pathlib import Path
import unittest

from check_ci_policy import check

WORKFLOW = (Path(__file__).resolve().parents[1] / 'workflows/validate.yml').read_text()


class PolicyTests(unittest.TestCase):
    def test_current_workflow(self):
        check(WORKFLOW)

    def test_privileged_trigger_is_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('pull_request:', 'pull_request_target:'))

    def test_shared_runner_group_is_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('group: macos-skill-isolated', 'group: Default'))

    def test_write_token_is_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('contents: read', 'contents: write'))

    def test_floating_action_is_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('11d5960a326750d5838078e36cf38b85af677262', 'v4'))

    def test_persisted_credentials_are_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('persist-credentials: false', 'persist-credentials: true'))

    def test_secrets_are_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW + '\nenv:\n  TOKEN: ${{ secrets.DEPLOY_TOKEN }}\n')

    def test_skipped_package_check_is_rejected(self):
        with self.assertRaises(AssertionError):
            check(WORKFLOW.replace('  package:\n', "  package:\n    if: github.event_name == 'push'\n"))


if __name__ == '__main__':
    unittest.main()
