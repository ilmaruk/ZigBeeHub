# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from zigbee_hub.persistence import commands

SleepEndDeviceJoin = namedtuple('SleepEndDeviceJoin', ['ieee_address', 'node_id'])

ReportAttributeCommand = namedtuple(
    'ReportAttributeCommand', ['node_id', 'end_point', 'cluster_id', 'attribute_id',
                               'data_type', 'attribute_value'])

ZoneStatusChangeNotificationCommand = namedtuple(
    'ZoneStatusChangeNotificationCommand', ['node_id', 'end_point', 'zone_status',
                                            'extend_status', 'zone_id', 'delay'])

ArmCommand = namedtuple('ArmCommand', ['node_id', 'end_point', 'arm_mode', 'arm_disarm_code', 'zone_id'])

EnrolRequestCommand = namedtuple(
    'EnrolRequestCommand', ['node_id', 'end_point', 'zone_type', 'manufacture_code'])

DefaultResponse = namedtuple(
    'DefaultResponse', ['node_id', 'end_point', 'cluster_id', 'command_id', 'status'])


def extract_data(prompt_type):
    def decorator(func):
        def wrapper(**kwargs):
            kwargs['prompt'] = prompt_type(*kwargs.get('payload').split(','))
            response = func(**kwargs)
            logging.info("Received {repr:s}".format(repr=str(kwargs.get('prompt'))))
            return response
        return wrapper
    return decorator


# def new_node_parser(payload):
#     nwk_addr, eui64, parent_nwk_addr = payload.split(",")
#     logging.info("NEWNODE prompt received with data {:s}".format(dict(nwk_addr=nwk_addr, eui64=eui64,
#                                                                       parent_nwk_addr=parent_nwk_addr)))
#     commands.register_device(eui64, nwk_addr)


# def received_raw_message_parser(payload):
#     logging.debug(payload)
#     headers, payload = payload.split(":")
#     src_nw_addr, profile_id, dest_ep, src_ep, cluster_id, payload_size = headers.split(",")
#     logging.info("RX prompt received with headers {:s}".format(dict(src_nw_addr=src_nw_addr, profile_id=profile_id,
#                                                                     dest_ep=dest_ep, src_ep=src_ep,
#                                                                     cluster_id=cluster_id, payload_size=payload_size)))
#     logging.debug(" ".join("{:02X}".format(ord(val)) for val in payload))


@extract_data(SleepEndDeviceJoin)
def sleep_end_device_join(**kwargs):
    info = kwargs.get('prompt')
    commands.register_device(info.ieee_address, info.node_id, "SED")


@extract_data(ReportAttributeCommand)
def report_attribute_command(**kwargs):
    command = kwargs.get('prompt')
    commands.register_telemetry(command.node_id, command.data_type, command.attribute_value)


@extract_data(ZoneStatusChangeNotificationCommand)
def zone_status_change_notification_command(**kwargs):
    command = kwargs.get('prompt')
    commands.register_heartbeat(command.node_id)


@extract_data(ArmCommand)
def arm_command(**kwargs):
    pass


@extract_data(EnrolRequestCommand)
def enroll_request_command(**kwargs):
    pass


@extract_data(DefaultResponse)
def default_response(**kwargs):
    pass

PROMPT_PARSERS = {
    "SED": sleep_end_device_join,
    "REPORTATTR": report_attribute_command,
    "ZONESTATUS": zone_status_change_notification_command,
    "ARM": arm_command,
    "ZENROLLREQ": enroll_request_command,
    "DFTREP": default_response,
}



