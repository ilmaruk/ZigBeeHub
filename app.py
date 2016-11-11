import argparse
import logging
import sys

from zigbee_hub.hub.configurations import SerialConf, HttpConf
from zigbee_hub.hub.hub import Hub


def parse_args():
    parser = argparse.ArgumentParser()

    # Serial arguments
    parser.add_argument('--serial-port', dest='serial_port', help='The serial port to connect to',
                        type=str, required=True)
    parser.add_argument('--serial-baud-rate', dest='serial_baud_rate', help='The serial baud rate',
                        type=int, default=19200)
    parser.add_argument('--serial-timeout', dest='serial_timeout', help='The serial timeout', type=int, default=1)

    # HTTP arguments
    parser.add_argument('--http-host', dest='http_host', help='The HTTP host to bind to',
                        default='0.0.0.0', type=str)  # NOSONAR
    parser.add_argument('--http-port', dest='http_port', help='The HTTP port to bind to', default=5000, type=int)

    return parser.parse_args()


def main(args):
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    hub = None

    try:
        serial_conf = SerialConf(args.serial_port, args.serial_baud_rate, args.serial_timeout)
        http_conf = HttpConf(host=args.http_host, port=args.http_port)
        hub = Hub(serial_conf, http_conf)
        hub.start()

    except TypeError as type_error:
        logging.error(str(type_error))
        if hub is not None:
            hub.stop()
        return 1

    return 0

if "__main__" == __name__:
    args = parse_args()
    sys.exit(main(args))
