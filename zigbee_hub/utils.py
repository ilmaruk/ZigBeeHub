# -*- coding: utf-8 -*-


class AtCommandBuilder(object):
    def __init__(self, command):
        self.command = command
        self.mandatory_params = []
        self.optional_params = []
        self.ignore_optionals = False

    def add_mandatory_param(self, format, value):
        self.mandatory_params.append(format.format(value))
        return self

    def add_optional_param(self, format, value):
        if value is None:
            self.ignore_optionals = True

        if self.ignore_optionals:
            return self

        self.optional_params.append(format.format(value))
        return self

    def build(self):
        command = self.command
        if self.mandatory_params or self.optional_params:
            command += ':' + ','.join(self.mandatory_params + self.optional_params)
        return str(command.upper())  # .upper() is not strictly necessary
