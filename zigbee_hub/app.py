import logging
import sys

from zigbee_hub.hub.configurations import SerialConf, HttpConf
from zigbee_hub.hub.hub import Hub


def main():
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    serial_conf = SerialConf('/dev/tty.SLAB_USBtoUART', 19200, 1)
    http_conf = HttpConf(host='0.0.0.0', port=5000)
    hub = Hub(serial_conf, http_conf)
    hub.start()

    return 0

if "__main__" == __name__:
    sys.exit(main())
