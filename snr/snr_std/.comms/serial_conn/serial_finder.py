""" This module seaches the operating system for devices on serial ports.

Likely based on pygame example code?
"""

import glob
import sys
import time
from sys import platform

import serial
from serial.serialutil import SerialBase
from snr.snr_core.base import *


class SerialFinder(Context):

    def __init__(self,
                 parent_context: Context,
                 ) -> None:
        super().__init__("serial_finder", parent_context)

    def find_port(self) -> Optional[str]:
        """ Finds a serial port for the serial connection
        """
        tries = 0
        port: Optional[str] = None
        while tries < self.settings.SERIAL_MAX_ATTEMPTS and not port:
            port = self.__get_port()
            if not port:
                time.sleep(self.settings.SERIAL_RETRY_WAIT)
            tries += 1
        return port

    def __get_port(self) -> Optional[str]:
        try:
            # Get a list of all serial ports
            self.dbg("Searching for serial ports")
            ports = self.__list_ports()
            self.dbg("Found ports:")
            for p in ports:
                self.dbg("{}", [p])
            # Select the port
            port = self.__select_port(ports)
            if not port:
                raise Exception("Serial Exception")
            self.dbg("Using port: {}", [port])
            return port

        except Exception as error:
            self.dbg("Error finding port: {}", [str(error)])
            return None

    def __list_ports(self) -> List[str]:
        """ Finds all serial ports and returns a list containing them

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif (sys.platform.startswith('linux')
              or sys.platform.startswith('cygwin')):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s: SerialBase = serial.serial(
                    port)    # Try to open a port
                s.close()                  # Close the port if sucessful
                result.append(port)        # Add to list of good ports
            except (OSError, Exception):   # If un sucessful
                pass
        return result

    def __select_port(self, ports: List[str]) -> Optional[str]:
        """ Selects the apprpriate port from the given list
        """
        if platform == "linux" or platform == "linux2":
            self.dbg("Linux detected")
            for p in ports:
                # return '/dev/ttyS0'
                # # If using raspi GPIO for serial, just pick this port
                if ("USB" in p) or ("ACM" in p):
                    return p

        elif platform == "darwin":
            self.dbg("Darwin detected")
            return ports[0]

        elif platform == "win32":
            self.dbg("Windows detected")
            p = ""
            for p in ports:
                self.dbg("{}", [p])
            return p
        return None
