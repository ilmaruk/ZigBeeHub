import sys
from functools import wraps

import flask
import serial
import time
from flask import Flask

from zigbee_hub.telegesis.r3xx_layout import Etrx3Usb, CommandError


def return_success(data):
    data["success"] = True
    return flask.jsonify(data)


def return_error(data):
    data["success"] = False
    return flask.jsonify(data), 500


def get_status(data):
    return 200 if data["success"] else 500


def track_response_time(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        start = time.time()
        data = dict()
        try:
            data["data"] = f(*args, **kwargs)
            data["success"] = True
        except CommandError as error:
            data = dict(success=False, error=error.get_code())
        finally:
            data["responseTime"] = time.time() - start
            return flask.jsonify(data), get_status(data)
    return wrapped


def main():
    hub = Flask(__name__)

    coordinator = Etrx3Usb(serial.Serial("/dev/ttyUSB0", 19200, timeout=1))

    @hub.route("/info", methods=["GET"])
    @track_response_time
    def get_info():
        return coordinator.info()

    @hub.route("/reset", methods=["GET", "PUT"])
    @track_response_time
    def put_reset():
        return coordinator.software_reset()

    @hub.route("/restore_factory_defaults", methods=["GET", "PUT"])
    @track_response_time
    def put_restore_factory_defaults():
        return coordinator.restore_factory_defaults()

    @hub.route("/establish_pan", methods=["GET", "PUT"])
    @track_response_time
    def put_establish_pan():
        return coordinator.establish_pan()

    @hub.route("/s_register_access/<register>", defaults={"bit": ""}, methods=["GET"])
    @hub.route("/s_register_access/<register>/<bit>", methods=["GET"])
    @track_response_time
    def get_s_register(register, bit):
        return coordinator.s_register_access(register, bit)

    hub.run()

    return 0

if "__main__" == __name__:
    sys.exit(main())
