# -*- coding: utf-8 -*-
import pytest
from pytest import fixture

from zigbee_hub.serial_reader import IncomingMessage


@fixture
def incoming_message():
    return "RX:eui64,node_id,profile_id,destination_endpoint,surce_endpoint,cluster_id,8:ciaociao"


@fixture
def incoming_message_no_eui64():
    return "RX:node_id,profile_id,destination_endpoint,surce_endpoint,cluster_id,8:ciaociao"


@fixture
def at_message():
    return "eui64,node_id,profile_id,destination_endpoint,surce_endpoint,cluster_id,8:ciaociao"


def test_should_tell_is_incoming_message(incoming_message):
    assert IncomingMessage.is_incoming_message(incoming_message) is True


def test_should_tell_is_not_incoming_message(at_message):
    assert IncomingMessage.is_incoming_message(at_message) is False


def test_should_set_eui64(incoming_message):
    assert IncomingMessage(incoming_message).eui64 == "eui64"


def test_should_not_set_eui64(incoming_message_no_eui64):
    assert IncomingMessage(incoming_message_no_eui64).eui64 is None


@pytest.mark.parametrize("message", [incoming_message(), incoming_message_no_eui64()])
def test_shoult_set_payload(message):
    assert IncomingMessage(message).length == 8
    assert IncomingMessage(message).payload == "ciaociao"
