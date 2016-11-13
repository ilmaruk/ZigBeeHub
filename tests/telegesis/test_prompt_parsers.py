# -*- coding: utf-8 -*-
from zigbee_hub.telegesis import prompt_parsers
from zigbee_hub.persistence import commands


def test_should_register_device_when_sleep_end_device_joins(mocker):
    mocker.patch('zigbee_hub.persistence.commands.register_device')
    prompt_parsers.sleep_end_device_join(payload='SED:0123456789ABCDEF,89AB')
    commands.register_device.assert_called_once_with('0123456789ABCDEF', '89AB', 'SED')


def test_should_register_telemetry_when_attribute_is_reported(mocker):
    mocker.patch('zigbee_hub.persistence.commands.register_telemetry')
    prompt_parsers.report_attribute_command(payload='REPORTATTR:89AB,02,0402,0000,29,0866')
    commands.register_telemetry.assert_called_once_with('89AB', '29', '0866')
