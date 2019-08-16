import os
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

SERVER_NAME = 'nginx-test.com'


def test_that_nginx_is_present(host):
    nginx_package = host.package('nginx')

    assert nginx_package.is_installed


def test_that_nginx_is_enabled(host):
    nginx_service = host.service('nginx')

    assert nginx_service.is_enabled


def test_that_nginx_has_a_working_configuration(host):
    cmd = host.run('nginx -t')

    assert cmd.rc == 0


def test_that_the_front_application_can_be_reached(host):
    cmd = host.run('curl 127.0.0.1/front/some/path' +
                   f"  --header 'Host: {SERVER_NAME}'")
    assert cmd.rc == 0

    answer = json.loads(cmd.stdout)
    assert answer['path'] == '/front/some/path'
    assert answer['appName'] == 'front-app'


def test_that_the_back_application_can_be_reached(host):
    cmd = host.run('curl 127.0.0.1/api/some/path' +
                   f"  --header 'Host: {SERVER_NAME}'")
    assert cmd.rc == 0

    answer = json.loads(cmd.stdout)
    assert answer['path'] == '/api/some/path'
    assert answer['appName'] == 'back-app'
