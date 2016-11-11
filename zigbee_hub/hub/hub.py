# -*- coding: utf-8 -*-
from Queue import Queue

import serial

from zigbee_hub.http import setup_http_interface
from zigbee_hub.serial_reader import SerialReader
from zigbee_hub.telegesis.r3xx_layout import Etrx3Usb

__author__ = 'Ruggero Ferretti <ruggero.ferretti@qton.com>'


class Hub(object):
    def __init__(self, serial_conf, http_conf):
        """
        :param serial_conf: the serial port configuration
        :type serial_conf: SerialConf
        :param serial_conf: the http interface configuration
        :type serial_conf: HttpConf
        """
        self.serial_conf = serial_conf
        self.http_conf = http_conf

        dongle = serial.Serial(serial_conf.port, serial_conf.baud_rate, timeout=serial_conf.timeout)
        at_queue = Queue()
        incoming_queue = Queue()

        self.coordinator = Etrx3Usb(dongle, at_queue)
        self.serial_reader = SerialReader(dongle, at_queue, incoming_queue)
        self.http_interface = setup_http_interface(self.coordinator)

    def start(self):
        self.serial_reader.start()
        self.http_interface.run(host=self.http_conf.host, port=self.http_conf.port)
