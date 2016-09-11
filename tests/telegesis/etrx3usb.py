import pytest
import serial

from mock import Mock
from zigbee_hub.telegesis.etrx3usb import Etrx3Usb


@pytest.fixture
def sut():
    return Etrx3Usb(Mock(spec=serial.Serial))


def read_line_mock():
    read_line_mock.line_counter += 1
    return read_line_mock.lines[read_line_mock.line_counter]


def test_should_get_info(sut, monkeypatch):
    monkeypatch.setattr(sut.serial_conn, "readline", read_line_mock)
    read_line_mock.lines = ["ATI\r\r\n", "device-name\r\n", "fw-revision\r\n", "ieee-id\r\n", "\r\n", "OK\r\n"]
    read_line_mock.line_counter = -1
    info = sut.info()
    assert info == dict(deviceName="device-name", firmwareRevision="fw-revision", ieeeIdentifier="ieee-id")


def test_should_do_reset(sut, monkeypatch):
    monkeypatch.setattr(sut.serial_conn, "readline", read_line_mock)
    read_line_mock.lines = ["ATZ\r\r\n", "JPAN:20,09AB,0123456789ABCDEF\r\n", "\r\n", "OK\r\n"]
    read_line_mock.line_counter = -1
    info = sut.do_software_reset()
    assert info == dict(jpan=dict(channel=20, pid="09AB", epid="0123456789ABCDEF"))


def test_should_establish_pan(sut, monkeypatch):
    monkeypatch.setattr(sut.serial_conn, "readline", read_line_mock)
    read_line_mock.lines = ["AT+EN\r\r\n", "JPAN:20,09AB,0123456789ABCDEF\r\n", "\r\n", "OK\r\n"]
    read_line_mock.line_counter = -1
    info = sut.establish_pan()
    assert info == dict(jpan=dict(channel=20, pid="09AB", epid="0123456789ABCDEF"))


def test_should_fail_establishing_pan(sut, monkeypatch):
    monkeypatch.setattr(sut.serial_conn, "readline", read_line_mock)
    read_line_mock.lines = ["AT+EN\r\r\n", "ERROR:12\r\n"]
    read_line_mock.line_counter = -1
    info = sut.establish_pan()
    assert info == dict(error=12)
