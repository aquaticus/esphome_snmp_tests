import pytest


def pytest_addoption(parser):
    parser.addoption("--chip", action="store", default="esp32", choices=['esp32', 'esp8266'])
    parser.addoption("--host", action="store", default="esphome-test-snmp-esp32.local")
    parser.addoption("--duration", action="store", type=int, default=60)


@pytest.fixture
def chip(request):
    return request.config.getoption("--chip")


@pytest.fixture
def host(request):
    return request.config.getoption("--host")


@pytest.fixture
def duration(request):
    return request.config.getoption("--duration")
