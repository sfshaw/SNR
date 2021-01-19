""" This module seaches the operating system for devices on serial ports
"""
# TODO: Find the origin of this code and give credit

import glob
import sys
from sys import platform
from typing import Callable, List, Optional

from snr_core.context.context import Context
from snr_core.utils.utils import attempt

import serial


class SerialFinder(Context):

    def __init__(self,
                 parent_context: Context,
                 set_port: Callable[[str], None]
                 ) -> None:
        super().__init__("serial_finder", parent_context)
        self.set_port = set_port

    def set_serial_port(self):
        """ Finds a serial port for the serial connection

        Calls the serial_finder library to search the operating system
        for serial ports
        """
        attempt(self.try_find_port,
                self.settings.SERIAL_MAX_ATTEMPTS,
                self.fail_once,
                self.failure)

    def try_find_port(self) -> bool:
        try:
            # Get a list of all serial ports
            self.dbg("Searching for serial ports")
            ports = self.__list_ports()
            self.dbg("Found ports:")
            for p in ports:
                self.dbg("{}", [p])
            # Select the port
            port = self.__select_port(ports)
            if(port is None):
                raise Exception("Serial Exception")
            self.set_port(port)
            self.dbg("Using port: {}", [port])
            return True

        except Exception as error:
            self.dbg("Error finding port: {}", [str(error)])
            return False

    def failure(self, tries: int) -> None:
        self.dbg("Could not find serial port after {} attempts. Crashing now.",
                 [tries])
        exit("Could not find port")

    def fail_once(self, e: Exception) -> None:
        self.dbg("Failed to find serial port, trying again.")
        # Wait a second before retrying
        self.sleep(self.settings.SERIAL_RETRY_WAIT)

        # return port

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
                s = serial.Serial(port)    # Try to open a port
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
