# -*- coding: utf-8 -*-
from zigbee_hub.utils import AtCommandBuilder


def parse_jpan(jpan):
    channel, pid, epid = jpan.split(":")[1].split(",")
    return channel, pid, epid


class Etrx3Usb(object):
    def __init__(self, serial_conn, serial_queue):
        """
        :param serial_conn:
        :type serial_conn: Serial
        """
        self.serial_conn = serial_conn
        self.serial_queue = serial_queue

    def send_command(self, command, timeout=10):
        # Unicode string are not supported
        self.serial_conn.write(str(command) + "\r\n")
        return self.serial_queue.get(True, timeout)

    def info(self):
        response = self.send_command("ATI")
        return dict(deviceName=response.next(), firmwareRevision=response.next(), ieeeIdentifier=response.next())

    def software_reset(self):
        response = self.send_command("ATZ")
        if response.has_data():
            channel, pid, epid = parse_jpan(response.next())
            return dict(jpan=dict(channel=int(channel), pid=pid, epid=epid))

        return dict()

    def restore_factory_defaults(self):
        self.send_command("AT&F")
        return dict()

    def establish_pan(self):
        response = self.send_command("AT+EN")
        if response.has_data():
            channel, pid, epid = parse_jpan(response.next())
            return dict(jpan=dict(channel=int(channel), pid=pid, epid=epid))

        return dict()

    def s_register_access(self, register, bit=""):
        register = register.zfill(2)
        response = self.send_command("ATS{register:s}{bit:s}?".format(register=register, bit=bit))
        return dict(sRegister=register, bit=bit, value=response.next())

    def permit_join(self, seconds=None, node_id=None):
        command = AtCommandBuilder('AT+PJOIN').\
            add_optional_param('{:02X}', seconds).\
            add_optional_param('{:s}', node_id).\
            build()
        response = self.send_command(command)
        return dict(value=response.next())
