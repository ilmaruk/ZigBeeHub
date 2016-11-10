# -*- coding: utf-8 -*-
import logging

from sqlalchemy.exc import IntegrityError

from zigbee_hub.persistence import session
from zigbee_hub.persistence import queries
from zigbee_hub.persistence.entities import Device, Temperature, Heartbeat


def register_device(eui64, node_id, type):
    device = Device()
    device.euid64 = eui64
    device.node_id = node_id
    device.type = type
    session.merge(device)
    try:
        session.commit()
        logging.debug("Device {eui64:s} successfully registered".format(eui64=eui64))
        return True

    except IntegrityError:
        session.rollback()
        logging.debug("Not registering device {eui64:s} as it already exists".format(eui64=eui64))
        return False


def set_device_type(eid64, node_id, dev_type):
    try:
        device = queries.get_device_by_pk(eid64)
        device.node_id = node_id
        device.type = dev_type
        session.commit()

    except Exception as error:
        session.rollback()


def register_telemetry(node_id, type, value):
    try:
        if type == "29":
            temperature = Temperature(node_id=node_id, value=int(value, 16) / 100.)
            session.add(temperature)
            session.commit()

        return True

    except IntegrityError:
        session.rollback()
        logging.debug("Not registering telemetry")
        return False


def register_heartbeat(node_id):
    try:
        session.merge(Heartbeat(node_id=node_id), load=True)
        session.commit()
        return True

    except IntegrityError:
        session.rollback()
        logging.debug("Not registering telemetry")
        return False
