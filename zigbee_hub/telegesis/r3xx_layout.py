def parse_jpan(jpan):
    channel, pid, epid = jpan.split(":")[1].split(",")
    return channel, pid, epid


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


class Etrx3Usb(object):
    def __init__(self, serial_conn):
        """
        :param serial_conn:
        :type serial_conn: Serial
        """
        self.serial_conn = serial_conn

    def send_command(self, command):
        self.serial_conn.write(command + "\r\n")
        response = CommandResponse()
        while True:
            line = self.serial_conn.readline().rstrip()
            if line == "OK":
                break
            elif line.startswith("ERROR"):
                raise CommandError(line)
            elif len(line) > 0 and line != command:
                response.add_line(line)

        return response

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
