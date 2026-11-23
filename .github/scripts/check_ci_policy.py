"""Regression checks for the public repository's CI trust boundary.

This checks workflow configuration, not VM or organization-policy isolation.
"""
from pathlib import Path
import re

import yaml

CHECKOUT = 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262'
ROUTE = {'group': 'macos-skill-isolated',
         'labels': ['self-hosted', 'Linux', 'X64', 'macos-skill-vm']}


def check(text):
    workflow = yaml.load(text, Loader=yaml.BaseLoader)
    assert set(workflow['on']) == {'pull_request', 'push', 'workflow_dispatch'}, 'Unexpected trigger'
    assert workflow['on']['push']['branches'] == ['main'], 'Push must target main'
    assert workflow['permissions'] == {'contents': 'read'}, 'Token must be read-only'
    assert not re.search(r'\bsecrets\s*[.\[]', text), 'No secrets in public CI'
    assert set(workflow['jobs']) == {'package'}, 'Review new jobs explicitly'
    job = workflow['jobs']['package']
    assert job['runs-on'] == ROUTE, 'Dedicated isolated runner group required'
    assert 0 < int(job['timeout-minutes']) <= 5, 'Bound job lifetime'
    assert not set(job) & {'if', 'container', 'services', 'permissions', 'environment', 'uses'}, 'Unexpected job capability or conditional skip'
    assert workflow['concurrency']['cancel-in-progress'] == 'true', 'Cancel superseded runs'
    checkout_count = 0
    for step in job['steps']:
        if 'uses' in step:
            assert step['uses'] == CHECKOUT, 'Only the reviewed pinned action is allowed'
            assert step.get('with', {}).get('persist-credentials') == 'false', 'Do not persist checkout credentials'
            checkout_count += 1
    assert checkout_count == 1, 'Exactly one checkout required'


if __name__ == '__main__':
    directory = Path(__file__).resolve().parents[1] / 'workflows'
    workflows = sorted(directory.glob('*.yml')) + sorted(directory.glob('*.yaml'))
    assert [path.name for path in workflows] == ['validate.yml'], 'Review added workflows explicitly'
    check(workflows[0].read_text())
    print('CI workflow policy passed; VM isolation requires separate operator evidence.')
