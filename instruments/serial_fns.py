#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing utility functions for serial communications.
"""

# IMPORTS #####################################################################

from __future__ import absolute_import
from __future__ import division

from serial.tools.list_ports import comports

# FUNCTIONS ###################################################################


class Device(object):
    """
    A device handler to compare against ListPortInfo objects generated by
    list_ports.comports()
    """
    def __init__(self, vid=None, pid=None, serial_number=None):
        super(Device, self).__init__()
        self.vid = vid
        self.pid = pid
        self.serial_number = serial_number

    def __eq__(self, other):
        """
        Compare this device against an ListPortInfo object. If the vid and
        pids match, and the serial_number either matches or is undefined,
        the port is equal to other, otherwise it is not equal.
        :param other: the device to compare against.
        :type other: ListPortInfo
        :return: The comparison.
        :rtype: `bool`
        """
        comparison = self.pid == other.pid and self.vid == other.vid
        if comparison and self.serial_number is not None:
            comparison = self.serial_number == other.serial_number
        return comparison

    @property
    def port(self):
        """
        Find the device in the list of ports
        :return: A string, representing the com port. On Windows, this is
        "COM_", on Linux, it is "/dev/tty_"
        :rtype: `str`
        """
        for port in comports():
            if self == port:
                try:
                    device = port.device
                except AttributeError as e:
                    raise AttributeError(e, " are you using pyserial 3.1+?")
                return device
