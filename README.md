# ansible-role-igtf

Ansible role for configuring [IGTF](https://www.igtf.net) Certificate
Authorities management.

This role is following the approach documented in [EGI's ansible style
guide](https://github.com/EGI-Foundation/ansible-style-guide).

## Requirements

None

## Role Variables

* `crl_deploy`: `true` for installing `fetch-crl` package

## Dependencies

None

## Example Playbook

```yaml
    - hosts: servers
      roles:
         - { role: EGI-Foundation.igtf }
```

## License

[MIT](LICENSE)

## Author Information

Please check [AUTHORS](AUTHORS).
