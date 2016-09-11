class Etrx3Usb(object):
    def __init__(self, serial_conn):
        """
        :param serial_conn:
        :type serial_conn: Serial
        """
        self.serial_conn = serial_conn

    def send_command(self, command):
        self.serial_conn.write(command + "\r\n")
        lines = []
        while True:
            line = self.serial_conn.readline().rstrip()
            if line == "OK":
                break
            elif line.startswith("ERROR"):
                return False, [line]
            elif len(line) > 0:
                lines.append(line)

        return True, lines

    def info(self):
        success, lines = self.send_command("ATI")
        return {
            "deviceName": lines[1],
            "firmwareRevision": lines[2],
            "ieeeIdentifier": lines[3]
        }

    def do_software_reset(self):
        success, lines = self.send_command("ATZ")
        data = {}
        if len(lines) > 1:
            channel, pid, epid = lines[1].split(":")[1].split(",")
            data["jpan"] = {
                "channel": int(channel),
                "pid": pid,
                "epid": epid
            }

        return data

    def do_restore_factory_defaults(self):
        self.send_command("AT&F")
        return {}

    def establish_pan(self):
        success, lines = self.send_command("AT+EN")
        data = {}
        if success and len(lines) > 1:
            channel, pid, epid = lines[1].split(":")[1].split(",")
            data["jpan"] = {
                "channel": int(channel),
                "pid": pid,
                "epid": epid
            }
        elif not success:
            _, error_code = lines[0].split(":")
            data["error"] = int(error_code)

        return data

