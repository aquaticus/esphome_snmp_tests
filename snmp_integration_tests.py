import re
import time

import pytest

from common import *


def test_walk(chip, host):
    all_oids = get_supported_oids(chip)

    oid_counter = 0
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('.1.3.6.1')),
        lookupMib=False
    )

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:

        if errorIndication:
            print(errorIndication)
            raise Exception(errorIndication)
        elif errorStatus:
            raise Exception('%s at %s' % (errorStatus.prettyPrint(),
                                          errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                oid = str(varBind[0])
                assert oid in all_oids
                oid_counter += 1

    assert oid_counter == len(all_oids)


class TestSystem:
    def test_descr(self, host):
        val = get_value("1.3.6.1.2.1.1.1.0", host)
        assert val.startswith('ESPHome version')

    def test_name(self, chip, host):
        val = get_value("1.3.6.1.2.1.1.5.0", host)
        if chip == 'esp32':
            assert val == 'esphome-test-snmp-esp32'
        else:
            assert val == 'esphome-test-snmp-esp8266'

    def test_services(self, host):
        val = get_value("1.3.6.1.2.1.1.7.0", host)
        assert val == '64'

    def test_contact(self, host):
        val = get_value("1.3.6.1.2.1.1.4.0", host)
        assert val == 'John Doe'

    def test_location(self, host):
        val = get_value("1.3.6.1.2.1.1.6.0", host)
        assert val == 'Cyberspace'

    def test_system_uptime(self, host):
        val1 = get_value("1.3.6.1.2.1.25.1.1.0", host)
        time.sleep(0.1)
        val2 = get_value("1.3.6.1.2.1.25.1.1.0", host)
        assert val2 > val1

    def test_network_uptime(self, host):
        val1 = get_value("1.3.6.1.2.1.1.3.0", host)
        time.sleep(0.1)
        val2 = get_value("1.3.6.1.2.1.1.3.0", host)
        assert val2 > val1


class TestStorageFlash:
    def test_index(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.1.1", host)
        assert val == '1'

    def test_description(self, host):
        val = get_value(".1.3.6.1.2.1.25.2.3.1.3.1", host)
        assert val == 'FLASH'

    def test_allocation_unit(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.4.1", host)
        assert val == '1'

    def test_size(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.5.1", host)
        assert int(val) > 4000000

    def test_used(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.6.1", host)
        assert int(val) > 400000


class TestStorageRam:
    def test_index(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.1.2", host)
        assert val == '2'

    def test_description(self, host):
        val = get_value(".1.3.6.1.2.1.25.2.3.1.3.2", host)
        assert val == 'SPI RAM'

    def test_allocation_unit(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.4.2", host)
        assert val == '1'

    def test_size(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.5.2", host)
        assert int(val) == 0

    def test_used(self, host):
        val = get_value("1.3.6.1.2.1.25.2.3.1.6.2", host)
        assert int(val) == 0

    def test_memory_size(self, chip, host):
        val = get_value("1.3.6.1.2.1.25.2.2", host)
        if chip == 'esp32':
            assert int(val) == 320
        else:
            assert int(val) == 160


class TestHeap:
    def test_size_esp32(self, chip, host):
        if chip != 'esp32':
            pytest.skip("Ignored for ESP8266 chip")

        val = get_value(CUSTOM_OID + "32.1.0", host)
        assert int(val) > 300000

    def test_free_esp32(self, chip, host):
        if chip != 'esp32':
            pytest.skip("Ignored for ESP8266 chip")

        val = get_value(CUSTOM_OID + "32.2.0", host)
        assert int(val) > 250000

    def test_min_free_esp32(self, chip, host):
        if chip != 'esp32':
            pytest.skip("Ignored for ESP8266 chip")

        val = get_value(CUSTOM_OID + "32.3.0", host)
        assert int(val) > 200000

    def test_max_free_esp32(self, chip, host):
        if chip != 'esp32':
            pytest.skip("Ignored for ESP8266 chip")

        val = get_value(CUSTOM_OID + "32.4.0", host)
        assert int(val) > 100000

    # EPS8266 only
    def test_free_esp8266(self, chip, host):
        if chip != 'esp8266':
            pytest.skip("Ignored for ESP32 chip")
        val = get_value(CUSTOM_OID + "8266.1.0", host)
        assert int(val) > 0

    def test_fragmentation_esp8266(self, chip, host):
        if chip != 'esp8266':
            pytest.skip("Ignored for ESP32 chip")
        val = get_value(CUSTOM_OID + "8266.2.0", host)
        assert int(val) > 0

    def test_max_free_esp8266(self, chip, host):
        if chip != 'esp8266':
            pytest.skip("Ignored for ESP32 chip")
        val = get_value(CUSTOM_OID + "8266.3.0", host)
        assert int(val) > 25000


class TestChip:
    def test_type_esp32(self, chip, host):
        val = get_value(CUSTOM_OID + "2.1.0", host)
        if chip == 'esp32':
            assert int(val) == 32
        else:
            assert int(val) == 8266

    def test_freq(self, chip, host):
        val = get_value(CUSTOM_OID + "2.2.0", host)
        if chip == 'esp32':
            assert int(val) == 240
        else:
            assert int(val) == 80

    def test_model(self, host):
        val = get_value(CUSTOM_OID + "2.3.0", host)
        assert len(val) > 0

    def test_cores(self, host):
        val = get_value(CUSTOM_OID + "2.4.0", host)
        assert int(val) >= 1

    def test_revision(self, host):
        val = get_value(CUSTOM_OID + "2.5.0", host)
        assert int(val) != 0


class TestWifi:
    def test_rssi(self, host):
        val = get_value(CUSTOM_OID + "4.1.0", host)
        assert int(val) < 0

    def test_bssi(self, host):
        val = get_value(CUSTOM_OID + "4.2.0", host)
        assert re.fullmatch(r'^[A-F0-9]{2}\:[A-F0-9]{2}\:[A-F0-9]{2}\:[A-F0-9]{2}\:[A-F0-9]{2}\:[A-F0-9]{2}$',
                            val) is not None

    def test_ssid(self, host):
        val = get_value(CUSTOM_OID + "4.3.0", host)
        assert len(val) > 0

    def test_ip(self, host):
        val = get_value(CUSTOM_OID + "4.4.0", host)
        assert re.fullmatch(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', val) is not None
