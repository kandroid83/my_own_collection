#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file with given content
version_added: "1.0.0"
description:
    - Creates a text file at C(path) with content C(content).
options:
    path:
        description: Full path to the file.
        required: true
        type: str
    content:
        description: Content to write.
        required: true
        type: str
author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create file
  my_own_module:
    path: /tmp/example.txt
    content: "Hello!"
'''

RETURN = r'''
path:
    description: Path of the created file.
    type: str
    returned: always
content:
    description: Written content.
    type: str
    returned: always
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )
    result = dict(changed=False, path='', content='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    path = module.params['path']
    content = module.params['content']
    result['path'] = path
    result['content'] = content

    current = ''
    if os.path.isfile(path):
        with open(path, 'r') as f:
            current = f.read()

    if not os.path.exists(path) or current != content:
        result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    if result['changed']:
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
