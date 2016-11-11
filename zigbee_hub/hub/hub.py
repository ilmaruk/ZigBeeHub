# -*- coding: utf-8 -*-
import logging
import socket
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

        self.serial_reader = None
        self.http_interface = None

    def start(self):

        try:
            dongle = serial.Serial(self.serial_conf.port, self.serial_conf.baud_rate, timeout=self.serial_conf.timeout)
            at_queue = Queue()
            incoming_queue = Queue()

            coordinator = Etrx3Usb(dongle, at_queue)
            self.serial_reader = SerialReader(dongle, at_queue, incoming_queue)
            self.http_interface = setup_http_interface(coordinator)

            self.serial_reader.start()
            self.http_interface.run(host=self.http_conf.host, port=self.http_conf.port)

            return 0

        except serial.SerialException as serial_error:
            logging.error(str(serial_error))
            return 1

        except socket.error as socket_error:
            self.stop_serial_reader()
            logging.error(str(socket_error))
            return 2

    def stop(self):
        self.stop_serial_reader()
        # self.stop_http_interface()

    def stop_serial_reader(self):
        if self.serial_reader is not None:
            self.serial_reader.stop()

    def stop_http_interface(self):
        if self.http_interface is not None:
            self.http_interface.stop()
