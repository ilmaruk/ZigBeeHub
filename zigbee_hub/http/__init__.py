# -*- coding: utf-8 -*-
import time
from functools import wraps

import flask
from flask import Flask
from flask import request

from zigbee_hub.serial_reader import CommandError


def setup_http_interface(coordinator):
    http_interface = Flask(__name__)

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

    @http_interface.route("/info", methods=["GET"])
    @track_response_time
    def get_info():
        return coordinator.info()

    @http_interface.route("/reset", methods=["GET", "PUT"])
    @track_response_time
    def put_reset():
        return coordinator.software_reset()

    @http_interface.route("/restore_factory_defaults", methods=["GET", "PUT"])
    @track_response_time
    def put_restore_factory_defaults():
        return coordinator.restore_factory_defaults()

    @http_interface.route("/establish_pan", methods=["GET", "PUT"])
    @track_response_time
    def put_establish_pan():
        return coordinator.establish_pan()

    @http_interface.route("/commands/permit_join", methods=["GET", "PUT"])
    @track_response_time
    def put_permit_join():
        seconds = request.values.get('seconds')
        node_id = request.values.get('node_id')
        return coordinator.permit_join(seconds=None if seconds is None else int(seconds), node_id=node_id)

    @http_interface.route("/s_register_access/<register>", defaults={"bit": ""}, methods=["GET"])
    @http_interface.route("/s_register_access/<register>/<bit>", methods=["GET"])
    @track_response_time
    def get_s_register(register, bit):
        return coordinator.s_register_access(register, bit)

    @http_interface.route("/command/<command>", methods=["GET"])
    @track_response_time
    def get_generic_command(command):
        return getattr(coordinator, command)()

    return http_interface
