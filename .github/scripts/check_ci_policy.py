"""Regression checks for the public repository's CI trust boundary.

This checks workflow configuration, not VM or organization-policy isolation.
"""
from pathlib import Path
import re

import yaml

CHECKOUT = 'actions/checkout@11d5960a326750d5838078e36cf38b85af677262'
ROUTE = {'group': 'macos-skill-isolated',
         'labels': ['self-hosted', 'Linux', 'X64', 'macos-skill-vm']}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(text):
    workflow = yaml.load(text, Loader=yaml.BaseLoader)
    require(set(workflow['on']) == {'pull_request', 'push', 'workflow_dispatch'}, 'Unexpected trigger')
    require(workflow['on']['push']['branches'] == ['main'], 'Push must target main')
    require(workflow['permissions'] == {'contents': 'read'}, 'Token must be read-only')
    require(not re.search(r'\bsecrets\s*[.\[]', text), 'No secrets in public CI')
    require(set(workflow['jobs']) == {'package'}, 'Review new jobs explicitly')
    job = workflow['jobs']['package']
    require(job['runs-on'] == ROUTE, 'Dedicated isolated runner group required')
    require(0 < int(job['timeout-minutes']) <= 5, 'Bound job lifetime')
    require(not set(job) & {'if', 'container', 'services', 'permissions', 'environment', 'uses'}, 'Unexpected job capability or conditional skip')
    require(workflow['concurrency']['cancel-in-progress'] == 'true', 'Cancel superseded runs')
    checkout_count = 0
    for step in job['steps']:
        if 'uses' in step:
            require(step['uses'] == CHECKOUT, 'Only the reviewed pinned action is allowed')
            require(step.get('with', {}).get('persist-credentials') == 'false', 'Do not persist checkout credentials')
            checkout_count += 1
    require(checkout_count == 1, 'Exactly one checkout required')


if __name__ == '__main__':
    directory = Path(__file__).resolve().parents[1] / 'workflows'
    workflows = sorted(directory.glob('*.yml')) + sorted(directory.glob('*.yaml'))
    require([path.name for path in workflows] == ['validate.yml'], 'Review added workflows explicitly')
    check(workflows[0].read_text())
    print('CI workflow policy passed; VM isolation requires separate operator evidence.')
