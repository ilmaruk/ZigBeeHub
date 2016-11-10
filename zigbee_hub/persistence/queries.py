# -*- coding: utf-8 -*-
from zigbee_hub.persistence import session
from zigbee_hub.persistence.entities import Device


def get_device_by_pk(eui64):
    return session.query(Device).filter(Device.euid64 == eui64).one()
