import time

from common import *


def get_all(host, chip):
    oid_all = get_supported_oids(chip)
    for oid in oid_all:
        get_value(oid, host)


def test_stability(chip, host, duration):
    if chip == 'esp32':
        min_heap_free = int(get_value(CUSTOM_OID + "32.3.0", host))  # min heap free
        print(f"Begin ESP32 min heap free: {min_heap_free}")
    else:
        heap_free = int(get_value(CUSTOM_OID + "8266.1.0", host))  # heap free
        print(f"Begin ESP8266 heap free: {heap_free}")

    start = time.time()
    while True:
        get_all(host, chip)
        diff = time.time() - start
        if diff >= duration:
            break

    if chip == 'esp32':
        min_heap_free = int(get_value(CUSTOM_OID + "32.3.0", host))  # min heap free
        print(f"End ESP32 min heap free: {min_heap_free}")
        assert heap_free > 100000  # set any safe value here
    else:
        heap_free = int(get_value(CUSTOM_OID + "8266.1.0", host))  # heap free
        print(f"End ESP8266 heap free: {heap_free}")
        assert heap_free > 100000  # set any safe value here
