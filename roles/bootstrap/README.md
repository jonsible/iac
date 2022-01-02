Role Name
=========

Bootstraping my servers

Requirements
------------

None

Role Variables
--------------

```yaml
default_user: "your_username" # Specify the username you want to be created
github_user: "your_github_username" # Your github username to retrieve your public SSH key
```

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: jonsible.iac.bootstrap }

License
-------

GPL-3.0-only

Author Information
------------------

Jonathan Scherrer
