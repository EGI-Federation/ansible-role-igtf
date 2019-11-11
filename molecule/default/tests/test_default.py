import os
import pytest
import re
from six.moves.urllib.request import urlopen
from xml.dom import minidom

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("repo_file,os_major_version", [
    ("EGI-trustanchors.repo", "6"),
    ("EGI-trustanchors.repo", "7"),
    ]
)
# Test that repositories are properly configured
def test_repositories_present(host, repo_file, os_major_version):
    f = host.file("/etc/yum.repos.d/"+repo_file)
    assert f.exists
    assert f.uid == 0
    assert f.group == 'root'


@pytest.mark.parametrize("repo_file", [
    ("EGI-trustanchors.repo"),
    ("EGI-trustanchors.repo"),
    ]
)
def test_repositories_enabled(host, repo_file):
    content = host.file("/etc/yum.repos.d/"+repo_file).content.decode('utf8')
    enabled_regex = re.compile(r'enabled\s*=\s*1')
    assert enabled_regex.search(content) is not None


def test_crl_files(host):
    cron = host.file('/etc/cron.d/fetch-crl')
    assert cron.exists
    assert cron.is_file


# def test_crl_freshness(host):


def test_egi_policy(host):
    ca_package_name = "ca-policy-egi-core"
    ca_package_version_url = ("http://repository.egi.eu/sw/production"
                              "/cas/1/current/release.xml")
    _doc = minidom.parse(urlopen(ca_package_version_url))
    _version = _doc.getElementsByTagName('Version')[0].firstChild.data
    ca_package_version = _version.split('-')[0]

    pkg = host.package(ca_package_name)
    assert pkg.is_installed
    assert pkg.version.startswith(ca_package_version)
