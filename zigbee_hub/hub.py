import sys

import flask
import serial
from flask import Flask

from zigbee_hub.telegesis.etrx3usb import Etrx3Usb


def success(data):
    data["success"] = True
    return flask.jsonify(data)


def error(data):
    data["success"] = False
    return flask.jsonify(data), 500


def main():
    app = Flask(__name__)

    coordinator = Etrx3Usb(serial.Serial("/dev/ttyUSB1", 19200, timeout=1))

    @app.route("/command/<command>", methods=["GET"])
    def execute_command(command):
        try:
            return success(getattr(coordinator, command)())
        except AttributeError:
            return error(dict(error="invalid command: {}".format(command)))

    @app.route("/info", methods=["GET"])
    def get_info():
        return flask.jsonify(coordinator.info())

    @app.route("/reset", methods=["GET", "PUT"])
    def put_reset():
        return flask.jsonify(coordinator.do_software_reset())

    @app.route("/restore_factory_defaults", methods=["GET", "PUT"])
    def put_restore_factory_defaults():
        return flask.jsonify(coordinator.do_restore_factory_defaults())

    @app.route("/establish_pan", methods=["GET", "PUT"])
    def put_establish_pan():
        return flask.jsonify(coordinator.establish_pan())

    app.run()

    return 0

if "__main__" == __name__:
    sys.exit(main())
