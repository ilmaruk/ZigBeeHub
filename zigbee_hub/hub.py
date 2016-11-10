import logging
import sys

import serial
from Queue import Queue

from zigbee_hub.http import setup_http_interface
from zigbee_hub.serial_reader import SerialReader
from zigbee_hub.telegesis.r3xx_layout import Etrx3Usb


def main():
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    dongle = serial.Serial("/dev/tty.SLAB_USBtoUART", 19200, timeout=1)
    at_queue = Queue()
    incoming_queue = Queue()

    coordinator = Etrx3Usb(dongle, at_queue)
    serial_reader = SerialReader(dongle, at_queue, incoming_queue)
    serial_reader.start()

    setup_http_interface(coordinator).run()

    return 0

if "__main__" == __name__:
    sys.exit(main())
