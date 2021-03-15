# """ This module manages the serial connection
# between the Pi and microcontroller
# TODO: Add more documentation here
# """

# import time

# import serial
# from serial.serialutil import SerialBase, SerialException
# from snr.core import *

# from .packet import *
# from .serial_finder import SerialFinder


# class SerialConnection(Endpoint):
#     # Default port arg finds a serial port for the arduino/Teensy
#     def __init__(self,
#                  factory: EndpointFactory,
#                  parent: NodeProtocol,
#                  name: str,
#                  input: str,
#                  ) -> None:
#         super().__init__(factory,
#                          parent,
#                          name)
#         self.task_handlers = {
#             (TaskType.event, "serial_com"):
#             self.handle_serial_com,
#             (TaskType.event, "blink_test"):
#             self.handle_blink_test
#         }
#         self.serial_connection: Optional[SerialBase] = None
#         if self.settings.SIMULATE_SERIAL:
#             self.simulated_bytes = None
#             return

#         self.dbg("Finding serial port")
#         self.port = SerialFinder(self).find_port()
#         self.info("Selected serial port {}", [self.serial_port])

#         self.attempt_connect()

#     def task_source(self) -> SomeTasks:
#         return None

#     def attempt_connect(self) -> None:
#         def fail_once() -> None:
#             self.warn("Failed to open serial port, trying again.")

#         def failure(e: Exception) -> None:
#             self.err("Could not open serial port after {} tries: {}",
#                      [self.settings.SERIAL_MAX_ATTEMPTS, e])
#             self.parent.schedule(
#                 tasks.terminate("serial_error"))

#         attempts = 0
#         self.serial_connection = self.try_open_serial()
#         while ((attempts < self.settings.SERIAL_MAX_ATTEMPTS) and
#                not self.serial_connection):
#             fail_once()
#             attempts += 1
#             self.serial_connection = self.try_open_serial()
#         if not self.serial_connection:
#             failure(Exception("Could not establish serial connection"))

#     def handle_serial_com(self, t: Task, k: TaskId) -> SomeTasks:
#         self.dbg("Executing serial com task: {}", [t.val_list])
#         result = self.send_receive(t.val_list[0],
#                                    t.val_list[1::])
#         if result:
#             return result
#         else:
#             self.dbg("Received no data in response from serial message")
#             return None

#     def handle_blink_test(self, t: Task, k: TaskId) -> None:
#         self.send_receive("blink", t.val_list)

#     def set_port(self, port: str) -> None:
#         self.dbg("Setting port to {}", [port])
#         self.serial_port = port

#     def try_open_serial(self) -> SerialBase:
#         if self.settings.SIMULATE_SERIAL:
#             self.dbg("serial_sim",
#                      "Not opening port", [])
#             raise Exception("Not opening serial port if simulating")
#         time.sleep(self.settings.SERIAL_SETUP_WAIT_PRE_S)
#         conn: SerialBase = serial.Serial(
#             port=self.serial_port,
#             baudrate=self.settings.SERIAL_BAUD,
#             parity=serial.PARITY_NONE,
#             stopbits=serial.STOPBITS_ONE,
#             bytesize=serial.EIGHTBITS,
#             timeout=self.settings.SERIAL_TIMEOUT)
#         if conn.isOpen():
#             self.info("Opened serial connection on {} at baud {}",
#                       [self.serial_port, self.settings.SERIAL_BAUD])
#             time.sleep(self.settings.SERIAL_SETUP_WAIT_POST)
#             waiting: int = conn.inWaiting()
#             while waiting > 0:
#                 if waiting > PACKET_SIZE:
#                     self.warn("Extra inbound bytes on serial: {}",
#                               [waiting])
#                 conn.read()
#                 waiting = conn.inWaiting()
#             return conn
#         raise Exception("Could not open serial connection")

#     # Send and receive data over serial
#     def send_receive(self,
#                      cmd_type: str,
#                      data: List[Any]
#                      ) -> SomeTasks:
#         t: List[Task] = []

#         if cmd_type.__eq__("blink"):
#             p = self.new_packet(BLINK_CMD, data[0], data[1])

#             self.send_receive_packet(p)
#         elif cmd_type.__eq__("set_motor"):
#             p = self.generate_motor_packet(data[0], data[1])

#             self.send_receive_packet(p)
#         elif cmd_type.__eq__("set_cam"):
#             p = self.new_packet(SET_CAM_CMD, data[0], 0)
#             self.send_receive_packet(p)
#         elif cmd_type.__eq__("read_sensor"):
#             pass
#         else:
#             self.err("Type of serial command {} not recognized",
#                      [cmd_type])
#             return None
#         return t

#     # Send and receive a serial packet
#     def send_receive_packet(self, p: SerialPacket) -> SerialPacket:
#         # send packet
#         self.write_packet(p)
#         # Recieve a packet from the Arduino/Teensy
#         p_recv = self.read_packet()
#         if p_recv is None:
#             self.dbg("serial_verbose", "Received an empty packet")
#         elif p.weak_eq(p_recv):
#             self.dbg("serial_verbose", "Received echo packet")
#         else:
#             self.dbg("serial_verbose", "Received {}", [p_recv])  # Debugging
#         return p

#     # Send a Packet over serial
#     def write_packet(self, p: SerialPacket) -> None:
#         data_bytes, expected_size = p.pack()
#         self.dbg("Trying to send packet of expected size {}",
#                  [expected_size])
#         sent_bytes = 0

#         if self.settings.SIMULATE_SERIAL:
#             self.dbg("Sending bytes {}", [data_bytes])
#             self.simulated_bytes = data_bytes
#             return

#         try:
#             if not self.serial_connection.isOpen():
#                 self.err("Aborting send, Serial is not open: {}",
#                          [self.serial_connection])
#                 return
#             sent_bytes += self.serial_connection.write(data_bytes)
#             self.dbg("Sent {} bytes: {}",
#                      [sent_bytes, data_bytes])
#             self.dbg("Out-waiting: {}",
#                      [self.serial_connection.out_waiting])
#         except SerialException as error:
#             self.err("Error sending packet: {}",
#                      [error.__repr__()])
#             return
#         self.dbg("Sent {}", [p])
#         return

#     # Read in a packet from serial
#     # TODO: ensure that this effectively recieves data over serial
#     def read_packet(self) -> Union[SerialPacket, None]:
#         if self.settings.SIMULATE_SERIAL:
#             self.dbg("Receiving packet of simulated bytes")
#             recv_bytes = self.simulated_bytes
#         else:
#             if not self.serial_connection.is_open:
#                 self.err("Aborting read, Serial is not open: {}",
#                          [self.serial_connection])
#                 return None
#             assert self.serial_connection
#             self.dbg("Waiting for bytes, %s ready",
#                      self.serial_connection.in_waiting)
#             tries = 0
#             while self.serial_connection.in_waiting < PACKET_SIZE:
#                 tries = tries + 1
#             self.dbg("Received enough bytes after %s tries", tries)
#             self.dbg("Reading, %s bytes ready",
#                      self.serial_connection.in_waiting)
#             try:
#                 recv_bytes = self.serial_connection.read(PACKET_SIZE)
#             except Exception as error:
#                 self.dbg("Error reading serial: {}",
#                          [error.__repr__()])
#         self.dbg("Read bytes from serial")
#         self.dbg("type(recv_bytes) = %s",
#                  type(recv_bytes))
#         cmd = int.from_bytes(recv_bytes[0], byteorder="little")
#         val1 = recv_bytes[1]
#         val2 = recv_bytes[2]
#         self.dbg("Unpacked: cmd: {}.{}, val1: {}.{}, val2: {}.{}"
#                  [cmd, cmd.__class__,
#                   val1, val1.__class__,
#                   val2, val2.__class__])
#         p = SerialPacket(cmd, val1, val2)
#         return p

#     def map_thrust_value(self, speed: int) -> int:
#         if speed > 100:
#             return 255
#         if speed < -100:
#             return 0
#         val = int((speed * 1.275) + 127)
#         self.dbg("Converted motor speed from {} to {}", [speed, val])
#         return val

#     def generate_motor_packet(self, motor: int, speed: int) -> SerialPacket:
#         mapped_speed = self.map_thrust_value(speed)
#         return self.new_packet(SET_MOT_CMD, motor, mapped_speed)

#     def new_packet(self, cmd: int, val1: int, val2: int):
#         """ Constructor for building packets to send (chksum is created)
#         """
#         self.dbg("Preparing packet: cmd: {}, val1: {}, val2: {}",
#                  [cmd, val1, val2])

#         return SerialPacket(cmd, val1, val2)

#     def make_packet(self, cmd: int, val1: int, val2: int):
#         """ Constructor for building packets (chksum is given)
#         """
#         return SerialPacket(cmd, val1, val2)

#     def terminate(self):
#         if self.serial_connection is not None:
#             self.dbg("Closing serial connection")
#             self.serial_connection.close()
#             self.serial_connection = None
#         self.dbg("Closed serial connection")
