"""
Runs Default tests
Available Modules: http://testinfra.readthedocs.io/en/latest/modules.html

"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    """
    Tests that the hosts file exists
    """
    file = host.file('/etc/ntp.conf')

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.contains('Ansible managed:')


def test_ntp_is_installed(host):
    """
    Tests that ntp is installed
    """
    ntp = host.package("ntp")
    assert ntp.is_installed


def test_ntp_running_and_enabled(host):
    """
    Tests that ntp is running and enabled
    """
    os_family = host.ansible("setup")["ansible_facts"]["ansible_os_family"]
    if os_family == "RedHat":
        ntp_service = "ntpd"
    elif os_family == "Debian":
        ntp_service = "ntp"

    ntp = host.service(ntp_service)
    assert ntp.is_running
    assert ntp.is_enabled
