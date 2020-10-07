"""Incomplete implementation of a thread function for consuming a
 multiprocessing Queue.

 Blockers: storing self.terminate flag
 Options: a. pass as a reference to func
          b. make consumer an object with that state
Recommendations: b. make consumer an object

Duplicate implementations already exist in dds.py and debug.py
"""
from multiprocessing import Queue
from queue import Empty
import threading
from snr.utils.debug.debug import CRITICAL_CHANNEL, DEBUG_CHANNEL, ERROR_CHANNEL, INFO_CHANNEL, WARNING_CHANNEL
from snr.utils.utils import format_message
from time import sleep
from threading import Thread
from typing import Any, Callable, List, Union


class Consumer:
    def __init__(self,
                 parent_name: str,
                 action: Callable,
                 sleep_time: float,
                 debugger=None):
        self.name = parent_name + "_consumer"
        self.dbgf = self.__printf
        if debugger:
            self.dbgf = debugger.debug
        self.action = action
        self.sleep_time = sleep_time
        self.queue: Queue[Any] = Queue()
        # self.start_flag = False
        self.terminate_flag = False
        self.thread = Thread(target=self.__loop, args=[], daemon=False)

        self.thread.start()

    # def start(self):
    #     self.dbgf(DEBUG_CHANNEL, "Starting thread")
    #     if self.is_alive():
    #         self.dbgf(CRITICAL_CHANNEL,
    #                   "Trying to start already running thread")
    #     self.start_flag = True
    #     self.thread.start()
    #     if not self.is_alive():
    #         self.dbgf(CRITICAL_CHANNEL,
    #                   "Started thread but not alive")

    def put(self, item: Any):
        self.check_alive("Consumer fed but thread is not alive")
        self.queue.put(item)

    def __loop(self):
        # if not self.start_flag:
        #     self.dbgf(CRITICAL_CHANNEL,
        #               "Thread not properly started, waiting for start()")
        #     while not self.start_flag:
        #         sleep(self.sleep_time)
        self.dbgf(DEBUG_CHANNEL, "Thread now running")
        if self.terminate_flag:
            self.dbgf(CRITICAL_CHANNEL,
                      "Thread expected to die instantly")
        while not self.terminate_flag:
            try:
                item = None
                item = self.queue.get_nowait()
                if item is not None:
                    self.action(item)
            except Empty:
                pass
            except EOFError as e:
                self.dbgf(ERROR_CHANNEL, f"EOFError: {e}")
                self.terminate_flag = True
            sleep(self.sleep_time)

        # Flush remaining lines
        try:
            item = None
            item = self.queue.get_nowait()
            while item is not None:
                self.action(item)
                item = None
                item = self.queue.get_nowait()
        except Empty:
            self.dbgf(DEBUG_CHANNEL, "Thread emptied queue")
        except Exception as e:
            self.dbgf(ERROR_CHANNEL, f"Failed to empty queue{e}")
        self.dbgf(DEBUG_CHANNEL, "Thread exited loop")

    def join(self):
        self.dbgf(INFO_CHANNEL, "Preparing to join thread")
        self.set_terminate_flag("join")
        self.catch_up()
        self.thread.join(timeout=0.75)
        if self.thread.is_alive():
            self.dbgf(WARNING_CHANNEL, "Thread just won't die.")

    def catch_up(self) -> None:
        MAX_TIME_WAITED = 5 * self.sleep_time
        time_waited = 0.0
        while (self.is_alive()
               and time_waited < MAX_TIME_WAITED
               and not self.queue.empty):
            sleep(self.sleep_time)
            time_waited += self.sleep_time
        self.dbgf(DEBUG_CHANNEL,
                  "Waited {} ms for consumer to catch up",
                  [time_waited * 1000])

    def set_terminate_flag(self, reason: str) -> None:
        self.terminate_flag = True

    def check_alive(self, message: str) -> None:
        if not self.is_alive():
            self.dbgf(DEBUG_CHANNEL, message, [self.name])

    def is_alive(self) -> bool:
        return(
            # self.start_flag and
            self.thread.is_alive())  # and not self.terminate_flag

    def __printf(self, level: str, *args: Union[List,  str]) -> None:
        print(format_message(self.name, level, *args))
