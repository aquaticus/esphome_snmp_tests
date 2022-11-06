from pysnmp.hlapi import *

CUSTOM_OID = ".1.3.9999."

supported_oids = [
    "1.3.6.1.2.1.1.1.0",
    "1.3.6.1.2.1.1.2.0",
    "1.3.6.1.2.1.1.3.0",
    "1.3.6.1.2.1.1.4.0",
    "1.3.6.1.2.1.1.5.0",
    "1.3.6.1.2.1.1.6.0",
    "1.3.6.1.2.1.1.7.0",
    "1.3.6.1.2.1.25.1.1.0",
    "1.3.6.1.2.1.25.2.2",
    "1.3.6.1.2.1.25.2.3.1.1.1",
    "1.3.6.1.2.1.25.2.3.1.1.2",
    "1.3.6.1.2.1.25.2.3.1.3.1",
    "1.3.6.1.2.1.25.2.3.1.3.2",
    "1.3.6.1.2.1.25.2.3.1.4.1",
    "1.3.6.1.2.1.25.2.3.1.4.2",
    "1.3.6.1.2.1.25.2.3.1.5.1",
    "1.3.6.1.2.1.25.2.3.1.5.2",
    "1.3.6.1.2.1.25.2.3.1.6.1",
    "1.3.6.1.2.1.25.2.3.1.6.2",
    "1.3.9999.2.1.0",
    "1.3.9999.2.2.0",
    "1.3.9999.2.3.0",
    "1.3.9999.2.4.0",
    "1.3.9999.2.5.0",
    "1.3.9999.4.1.0",
    "1.3.9999.4.2.0",
    "1.3.9999.4.3.0",
    "1.3.9999.4.4.0",
]

esp32_oids = ["1.3.9999.32.1.0", "1.3.9999.32.2.0", "1.3.9999.32.3.0", "1.3.9999.32.4.0", ]

esp8266_oids = ["1.3.9999.8266.1.0", "1.3.9999.8266.2.0", "1.3.9999.8266.3.0", ]


def get_supported_oids(chip):
    if chip == 'esp32':
        all_oids = supported_oids + esp32_oids
    else:
        all_oids = supported_oids + esp8266_oids

    return all_oids


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = str(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def snmp_get(oid, host):
    iterator = getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((host, 161)), ContextData(),
        ObjectType(ObjectIdentity(oid)))

    return fetch(iterator, 1)[0]


def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(ObjectType(ObjectIdentity(key), value))
    return pairs


def get_value(oid, host):
    return list(snmp_get(oid, host).values())[0]
