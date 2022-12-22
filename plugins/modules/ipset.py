#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipset

short_description: Manage ipsets

version_added: "1.0.0"

description: Module to manage ipsets

options:
    name:
        description: The ipset name
        required: true
        type: str
    type:
        description: The ipset type
        required: false
        type: str
        default: hash:ip
    create:
        description: Create the ipset
        required: false
        type: bool
        default: true
    entry:
        description: The entry to add or remove
        required: true
        type: str
    state:
        description: The entry state
        required: false
        default: present
        choices: [ present, absent, destroyed ]
author:
    - Jonathan Scherrer (@joscherrer)
"""

EXAMPLES = r"""
# Create a set
- name: Create a set
  jonsible.iac.ipset:
    name: "known"
    type: "hash:ip"

# Add an entry to a set
- name: Add an entry to a set
  jonsible.iac.ipset:
    name: "dns"
    type: "hash:ip"
    entry: "8.8.8.8"
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
stdout:
    description: The standard output of the ipset command.
    type: str
    returned: always
    sample: ''
stderr:
    description: The standard error of the ipset command.
    type: str
    returned: always
    sample: 'ipset v7.15: Kernel error received: Operation not permitted'
"""

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        name=dict(type="str", required=True),
        type=dict(type="str", required=False, default="hash:ip"),
        create=dict(type="bool", required=False, default=True),
        entry=dict(type="str", required=False),
        state=dict(
            type="str",
            required=False,
            default="present",
            choices=["present", "absent", "destroyed"],
        ),
    )

    result = dict(changed=False, failed=False, created=False, stdout="", stderr="")
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    # Test if the ipset exists
    rc, stdout, _ = module.run_command(f"ipset list {module.params['name']} -name")
    ipset_exists = True if stdout.strip() == module.params["name"] else False

    # Nothing to do
    if not ipset_exists and module.params["state"] == "destroyed":
        module.exit_json(**result)

    # Destroy the ipset
    if ipset_exists and module.params["state"] == "destroyed":
        cmd = f"ipset destroy {module.params['name']}"
        rc, stdout, stderr = module.run_command(cmd)
        if rc != 0:
            result["stdout"] = stdout
            result["stderr"] = stderr
            result["cmd"] = cmd
            module.fail_json(msg="Failed to destroy ipset", **result)
        result["changed"] = True
        module.exit_json(**result)

    # Create the ipset
    if not ipset_exists and module.params["create"]:
        rc, stdout, stderr = module.run_command(
            f"ipset create {module.params['name']} {module.params['type']}"
        )
        if rc != 0:
            result["stdout"] = stdout
            result["stderr"] = stderr
            result["cmd"] = cmd
            module.fail_json(msg="Failed to create ipset", **result)
        result["changed"] = True

    if module.params["entry"] is None:
        module.exit_json(**result)

    # Test if the entry is already in the ipset
    rc, stdout, stderr = module.run_command(
        f"ipset test {module.params['name']} {module.params['entry']}"
    )
    entry_exists = True if rc == 0 else False

    # Add the entry
    if not entry_exists and module.params["state"] == "present":
        cmd = f"ipset add {module.params['name']} {module.params['entry']}"
        rc, stdout, stderr = module.run_command(cmd)
        if rc != 0:
            result["stdout"] = stdout
            result["stderr"] = stderr
            result["cmd"] = cmd
            module.fail_json(msg="Failed to add entry", **result)
        result["changed"] = True

    # Remove the entry
    if entry_exists and module.params["state"] == "absent":
        cmd = f"ipset del {module.params['name']} {module.params['entry']}"
        rc, stdout, stderr = module.run_command(cmd)
        if rc != 0:
            result["stdout"] = stdout
            result["stderr"] = stderr
            result["cmd"] = cmd
            module.fail_json(msg="Failed to delete entry", **result)
        result["changed"] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
