cephadm-ansible
===================
**Automate deploying Ceph using cephadm and docker at scale**

About
===================
[cephadm-ansible] exists to utilize the upstream [Ceph Orchestrator]
and its SSH module wrapped in an Ansible playbook that deploys and
isolates services using [docker]. The intention is to explore creating
an alternative to [ceph-ansible] that more closely aligns with the
needs and deployment strategy employed by [kolla-ansible].

This playbook will allow a user to deploy a standalone [Ceph] cluster
that trivializes integrating with [kolla-ansible], and follows
official [Ceph] recommended practices by default.

Goals
===================
* Deploying must be relatively trivial, with clear directions
* Purging a cluster must revert _all_ changes, with _no_ side effects
* Updating must be seemless, regardless of minor/patch version changes
* Upgrading must be seemless, regardless of major version changes
* All of the above must also work **flawlessly** with [kolla-ansible]

Platform Support
==============================
| Operating System   | Quality |
| ------------------ | ------- |
| Alpine Linux 3.11+ | None, planned
| CentOS 8.x+        | None, planned
| Ubuntu 20.04LTS+   | None, planned


Usage
===================

Caveats
-------------------
Before we go into too much detail, let's clarify the locations of
common Ansible files/folders as they have been changed to reduce
clutter in the top-level directory.  While this is entirely arbitrary
and adding confusion, the tradeoff of having a subjectively "cleaner"
repository will (hopefully) be a net benefit.

Here's a rough legend for explaining the altered hierarchy, or at
least what is non-standard:

```sh
$ tree
.
├── modules         # ie 'library'
├── plays           # arbitrary location for site.*.yml files
├── plugins
│   ├── actions     # ie 'action_plugins'
│   ├── callbacks   # ie 'callback_plugins'
│   └── filters     # ie 'filter_plugins'
└── vars
    ├── groups      # ie 'group_vars'
    └── hosts       # ie 'host_vars'
```

Quick Start
-------------------

1. Check for any potential issues
```sh
$ ansible-playbook play/check.yml
```

2. Deploy this playbook
```sh
$ ansible-playbook play/deploy.yml
```

3. Upgrade the deployment
```sh
$ ansible-playbook play/upgrade.yml
```

3. Downgrade the deployment
```sh
$ ansible-playbook play/downgrade.yml
```

5. Tear the deployment down
```sh
$ ansible-playbook play/purge.yml
```

Methodology
==============================
A loose, un-ordered series of notes about how things are designed.

* All variables are prefixed with `ceph_*`, hopefully allowing this
  playbook to be imported into others without much hassle.
* There's no point in making gratuitous re-declarations of BlueStore
  defaults.  If Ceph has default settings, **use them**.
* If anything can be calculated reliably, do some math rather than
  providing a list or range of options.
* Before deploying, users must feel safe that our `check.yml` play
  caught any potential issues.


[ceph]: ceph.com
[ceph orchestrator]: https://docs.ceph.com/docs/master/mgr/orchestrator_cli/
[ceph-ansible]: https://github.com/ceph/ceph-ansible
[cephadm]: https://docs.ceph.com/docs/master/bootstrap
[cephadm-ansible]: https://github.com/jcmdln/cephadm-ansible
[kolla-ansible]: https://github.com/openstack/kolla-ansible
