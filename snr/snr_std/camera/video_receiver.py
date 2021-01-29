""" Requires OpenCV2:
https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html
"""

import pickle
import socket
import struct

import cv2
import numpy as np
from snr.snr_core.base import *
from snr.snr_std.cv import find_plants
from snr.snr_std.cv.boxes import apply_boxes

HOST = "localhost"

# Number of frames to skip to calculate the box
FRAME_SKIP_COUNT = 5

# Title of the window
WINDOW_TITLE = 'Video'

TICK_RATE_HZ = 0.0  # never sleep the server


class VideoReceiver(ThreadLoop):
    """Video stream receiving endpoint.
    Shows video received over IP in window.
    """

    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 name: str,
                 receiver_port: int
                 ) -> None:
        super().__init__(factory,
                         parent,
                         name,
                         TICK_RATE_HZ)
        self.receiver_port = receiver_port
        self.window_name = f"Raspberry Pi Stream: {self.name}"
        self.count = 0  # Frame count
        self.boxes = []  # Cache of cv boxes
        self.start()

    def setup(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dbg("{}: Socket created on {}",
                     [self.name, self.receiver_port])

            self.s.bind((HOST, self.receiver_port))
            self.s.listen(10)
            self.dbg("{}: Socket now listening/blocking on {}",
                     [self.name, self.receiver_port])
            self.conn, self.addr = self.s.accept()
        except (Exception, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                raise(e)
            else:
                self.set_terminate_flag()
                return

        self.data = b''
        self.payload_size = struct.calcsize("=L")

    def loop_handler(self):
        try:
            # Retrieve message size
            while len(self.data) < self.payload_size:
                self.data += self.conn.recv(4096)

            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            msg_size = struct.unpack("=L", packed_msg_size)[0]

            # Retrieve all data based on message size
            while len(self.data) < msg_size:
                self.data += self.conn.recv(4096)

            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]

            # Extract frame
            frame: np.array = pickle.loads(frame_data)

            self.count += 1

            # Select frames for processing
            if ((self.count % FRAME_SKIP_COUNT) == 0):
                self.boxes = find_plants.box_image(frame)
            # This control flow applies old boxes to new frames
            frame = apply_boxes(frame,
                                self.boxes,
                                find_plants.color,
                                find_plants.LINE_THICKNESS)

            # Display
            cv2.imshow(self.window_name, frame)
            cv2.waitKey(15)
        except (Exception, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                raise(e)
            self.err("camera_error",
                     f"receiver monitor error: {e}",)
            self.set_terminate_flag(f"Exception: {e}")

    def terminate(self):
        cv2.destroyAllWindows()

        if self.s is not None:
            self.s.close()

        if self.count > 0:
            self.parent.store_data(f"{self.name}_recvd_frames",
                                   self.count)
            self.dump("Total frames recvd: {}",
                      [self.count])
