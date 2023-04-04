# Esphome tests for SNMP component

The project provides integration tests for SNMP component.
It uses `pytest` Python test framework.

SNMP Component source code: https://github.com/aquaticus/esphome/tree/aquaticus-snmp

SNMP Component documentation: https://aquaticus.info/snmp.html

# Preparation

First create a new file and call it `secret.yaml`.
Add the following content and modify appropriate lines to match you config.

```yaml
api_pass: "<API PASS>"
ota_pass: "<OTA PASS>"
wifi_ssid: "<WIFI SSID>"
wifi_pass: "<WIFI PASS>"
```

There are two `yaml` files one for ESP32 and one for ESP8266.
By default, board type is set to `d1_mini` (ESP8266) or `wemos_d1_mini32` (ESP32).
You can modify `board` token to march your test equipment. 

Compile and upload test project to ESP32 and/or ESP8266 board.

Install additional Python modules:
```shell
pip install -r requirements.txt
```

## ESP32
```shell
esphome run esphome-test-snmp-esp32.yaml
```

## ESP8266
```shell
esphome run esphome-test-snmp-esp8266.yaml
```

# Run tests

Tests accepts 3 (optional) arguments:
* `--chip` - chip type: `esp32` or `esp8266`; default `esp32`
* `--host` - host name or IP address of the board; default `esphome-test-snmp-esp32.locale`
* `--duration` - time in seconds for stability test; default 60s

# ESP32

Runs integrity tests.

```shell
pytest --chip esp32 --host esphome-test-snmp-esp32.locale  snmp_integration_tests.py
```

# ESP8266

Runs integrity tests.

```shell
pytest --chip esp32 --host esphome-test-snmp-esp8266.locale  snmp_integration_tests.py
```

For more detailed description how to run tests look at [pytest documentation](https://docs.pytest.org/en/7.2.x/contents.html).
