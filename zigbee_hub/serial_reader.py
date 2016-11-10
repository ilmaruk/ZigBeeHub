# -*- coding: utf-8 -*-
import logging
import re
import threading

from zigbee_hub.telegesis.prompt_parsers import PROMPT_PARSERS


class IncomingMessage(object):
    @staticmethod
    def is_incoming_message(message):
        """
        :param message: the message
        :type message: unicode
        """
        return message.startswith("RX:")

    def __init__(self, message):
        """
        < EUI64 >, < NWK addr >, < profileID >, < destinationEndpoint >, < SourceEndpoint >, < clusterID >, < length >: < payload >
        :param message: the message
        :type message: unicode
        """
        parts = message.lstrip("RX:").split(",")
        if len(parts) == 7:
            self.eui64, self.mwk_addr, self.profile_id, self.destination_endpoint, self.source_endpoint, self.cluster_id, payload = parts
        else:
            self.mwk_addr, self.profile_id, self.destination_endpoint, self.source_endpoint, self.cluster_id, payload = parts
            self.eui64 = None
        self.length = int(payload.split(":")[0])
        self.payload = payload.split(":")[1]


class CommandError(Exception):
    def __init__(self, error_line):
        self.code = int(error_line.split(":")[1])

    def get_code(self):
        return self.code


class CommandResponse(object):
    def __init__(self):
        self.lines = list()
        self.index = -1

    def add_line(self, line):
        self.lines.append(line)

    def has_data(self):
        return len(self.lines) > 0

    def get(self, index):
        self.index = index
        return self.lines[index]

    def next(self):
        self.index += 1
        return self.lines[self.index]


class SerialReader(threading.Thread):

    def __init__(self, serial_conn, at_queue, incoming_queue):
        """
        :param serial_conn:
        :type serial_conn: Serial
        """
        super(SerialReader, self).__init__()
        self.serial_conn = serial_conn
        self.at_queue = at_queue
        self.incoming_queue = incoming_queue

    def run(self):
        pattern = re.compile(r"^[A-Za-z]+:")
        response = CommandResponse()

        while True:
            line = self.serial_conn.readline().rstrip()
            if line == "OK":
                self.at_queue.put(response)
                response = CommandResponse()
            elif pattern.match(line):
                self.parse_prompt(line)
            elif IncomingMessage.is_incoming_message(line):
                self.incoming_queue.put(IncomingMessage(line))
            elif line.startswith("ERROR"):
                raise CommandError(line)
            elif len(line) > 0:
                response.add_line(line)

    @staticmethod
    def parse_prompt(prompt):
        prompt_command, prompt_payload = prompt.split(":", 1)
        parser = PROMPT_PARSERS.get(prompt_command)
        if parser is None:
            logging.warn("Unsupported prompt: {:s}".format(prompt_command))
            return
        parser(payload=prompt_payload)
