# -*- coding: utf-8 -*-
from collections import namedtuple

__author__ = 'Ruggero Ferretti <ruggero.ferretti@qton.com>'


SerialConf = namedtuple('SerialConf', ['port', 'baud_rate', 'timeout'])

HttpConf = namedtuple('HttpConf', ['host', 'port'])
