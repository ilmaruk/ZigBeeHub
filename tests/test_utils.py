# -*- coding: utf-8 -*-
from zigbee_hub.utils import AtCommandBuilder

__author__ = 'Ruggero Ferretti <ruggero.ferretti@qton.com>'


def test_should_build_command_without_params():
    builder = AtCommandBuilder('cmd')
    assert builder.build() == 'CMD'


def test_should_build_command_with_mandatory_param():
    builder = AtCommandBuilder('cmd').\
        add_mandatory_param('{:02X}', 10)
    assert builder.build() == 'CMD:0A'


def test_should_build_command_with_mandatory_params():
    builder = AtCommandBuilder('cmd').\
        add_mandatory_param('{:02X}', 10).\
        add_mandatory_param('{:s}', '89ab')
    assert builder.build() == 'CMD:0A,89AB'


def test_should_build_command_without_optional_param():
    builder = AtCommandBuilder('cmd').\
        add_mandatory_param('{:02X}', 10).\
        add_mandatory_param('{:s}', '89ab').\
        add_optional_param('{:d}', None)
    assert builder.build() == 'CMD:0A,89AB'


def test_should_build_command_with_optional_param():
    builder = AtCommandBuilder('cmd').\
        add_mandatory_param('{:02X}', 10).\
        add_mandatory_param('{:s}', '89ab').\
        add_optional_param('{:d}', 10)
    assert builder.build() == 'CMD:0A,89AB,10'


def test_should_build_command_without_optional_params():
    builder = AtCommandBuilder('cmd').\
        add_mandatory_param('{:02X}', 10).\
        add_mandatory_param('{:s}', '89ab').\
        add_optional_param('{:d}', None).\
        add_optional_param('{:d}', 10)
    assert builder.build() == 'CMD:0A,89AB'
