#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule


def bootstrap(r, m):
    # Check if 'mon_ip' is an empty string first so we can error as
    # early as possible.
    if not m.params["mon_ip"]:
        r["rc"] = 1
        r["msg"] = (
            "'mon_ip' cannot be an empty string.  Please use the IP",
            "address of the host to bootstrap.",
        )
        return r
    else:
        r["command"] = "%s --mon-ip %s" & (r["command"], r["mon_ip"])

    if r["allow_fqdn_hostname"]:
        r["command"] = "%s --allow-fqdn-hostname" % r["command"]

    if r["allow_overwrite"]:
        r["command"] = "%s --allow-overwrite" % r["command"]

    if r["config"]:
        r["command"] = "%s --config %s" % (r["command"], r["config"])

    if r["fsid"]:
        r["command"] = "%s --fsid %s" % (r["command"], r["fsid"])

    if r["mgr_id"]:
        r["command"] = "%s --mgr-id %s" % (r["command"], r["mgr_id"])

    if r["mon_addrv"]:
        r["command"] = "%s --mon-addrv %s" % (r["command"], r["mon_addrv"])

    if r["mon_id"]:
        r["command"] = "%s --mon-id %s" % (r["command"], r["mon_id"])

    if r["no_minimize_config"]:
        r["command"] = "%s --no-minimize-config" % r["command"]

    if r["orphan_initial_daemons"]:
        r["command"] = "%s --orphan-initial-daemons" % r["command"]

    if r["output_config"]:
        r["command"] = "%s --output-config %s" % (r["command"], r["output_config"])

    if r["output_dir"]:
        r["command"] = "%s --output-dir %s" % (r["command"], r["output_dir"])

    if r["output_keyring"]:
        r["command"] = "%s --output-keyring %s" % (r["command"], r["output_keyring"])

    if r["output_pub_ssh_key"]:
        r["command"] = "%s --output-pub-ssh-key %s" % (
            r["command"],
            r["output_pub_ssh_key"],
        )

    if r["skip_dashboard"]:
        r["command"] = "%s --skip-dashboard" % r["command"]
    else:
        if r["dashboard_crt"]:
            r["command"] = "%s --dashboard-crt %s" % (r["command"], r["dashboard_crt"])

        if r["dashboard_key"]:
            r["command"] = "%s --dashboard-key %s" % (r["command"], r["dashboard_key"])

        if r["dashboard_password_noupdate"]:
            r["command"] = "%s --dashboard-password-noupdate" % (r["command"])

        if r["initial_dashboard_user"]:
            r["command"] = "%s --initial-dashboard-user %s" % (
                r["command"],
                r["initial_dashboard_user"],
            )

        if r["initial_dashboard_password"]:
            r["command"] = "%s --initial-dashboard-password %s" % (
                r["command"],
                r["initial_dashboard_password"],
            )

    if r["skip_firewalld"]:
        r["command"] = "%s --skip-firwalld" % r["command"]

    if r["skip_mon_network"]:
        r["command"] = "%s --skip-mon-network" % r["command"]

    if r["skip_monitoring_stack"]:
        r["command"] = "%s --skip-monitoring-stack" % r["command"]

    if r["skip_ping_check"]:
        r["command"] = "%s --skip-ping-check" % r["command"]

    if r["skip_prepare_host"]:
        r["command"] = "%s --skip-prepare-host" % r["command"]

    if r["skip_pull"]:
        r["command"] = "%s --skip-pull" % r["command"]

    if r["skip_ssh"]:
        r["command"] = "%s --skip-ssh" % r["command"]

    # Run the command, catching any stdout/stderr
    r["rc"], r["stdout"], r["stderr"] = m.run_command(r["command"], check_rc=False)

    if r["rc"] > 0:
        r["changed"] = True
        r["msg"] = "received a non-zero exit code"

    return r


def main():
    module = AnsibleModule(
        argument_spec={
            "allow_fqdn_hostname": {"type": "bool", "default": False},
            "allow_overwrite": {"type": "bool", "default": False},
            "config": {"type": "str", "default": ""},
            "dashboard_crt": {"type": "str", "default": ""},
            "dashboard_key": {"type": "str", "default": ""},
            "dashboard_password_noupdate": {"type": "bool", "default": False},
            "fsid": {"type": "str", "default": ""},
            "initial_dashboard_user": {"type": "str", "default": ""},
            "initial_dashboard_password": {"type": "str", "default": ""},
            "mgr_id": {"type": "str", "default": ""},
            "mon_addrv": {"type": "str", "default": ""},
            "mon_id": {"type": "str", "default": ""},
            "mon_ip": {"type": "str", "default": ""},
            "no_minimize_config": {"type": "bool", "default": False},
            "orphan_initial_daemons": {"type": "bool", "default": False},
            "output_config": {"type": "str", "default": ""},
            "output_dir": {"type": "str", "default": ""},
            "output_keyring": {"type": "str", "default": ""},
            "output_pub_ssh_key": {"type": "str", "default": ""},
            "skip_dashboard": {"type": "bool", "default": False},
            "skip_firewalld": {"type": "bool", "default": False},
            "skip_mon_network": {"type": "bool", "default": False},
            "skip_monitoring_stack": {"type": "bool", "default": False},
            "skip_ping_check": {"type": "bool", "default": False},
            "skip_prepare_host": {"type": "bool", "default": False},
            "skip_pull": {"type": "bool", "default": False},
            "skip_ssh": {"type": "bool", "default": False},
        },
        mutually_exclusive=[
            ["skip_dashboard", "dashboard_crt"],
            ["skip_dashboard", "dashboard_key"],
            ["skip_dashboard", "dashboard_password_noupdate"],
            ["skip_dashboard", "initial_dashboard_user"],
            ["skip_dashboard", "initial_dashboard_password"],
        ],
        required_one_of=[["mon_ip"]],
    )

    result = {
        "changed": False,
        "command": "cephadm bootstrap",
        "msg": "no action performed",
        "rc": 0,
        "stderr": "",
        "stdout": "",
    }

    result = bootstrap(result, module)

    if result["rc"] > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
