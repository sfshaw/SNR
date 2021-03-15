import time
import unittest

from snr import *
from snr.core.contexts.profiler import Profiler

SLEEP_TIME_S: float = 0.00005


class TestProfiler(unittest.TestCase):

    def test_no_operations(self):
        profiler: AbstractProfiler = Profiler(Settings())
        profiler.join_from("test_complete")
        profiler.dump()

    def test_profiler_start_join(self):
        prof: AbstractProfiler = Profiler(Settings())

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(prof.is_alive())

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(prof.is_alive())

        prof.join_from("test complete")
        self.assertFalse(prof.is_alive())
        time.sleep(CATCH_UP_TIME_S)
        self.assertFalse(prof.is_alive())

    def test_profiler_put(self):

        profiler = Profiler(Settings())

        def flush() -> None:
            if profiler.is_alive():
                time.sleep(SLEEP_TIME_S * 10)
                profiler.flush()
                time.sleep(SLEEP_TIME_S * 10)
                profiler.flush()

        try:
            flush()
            self.assertTrue(profiler.is_alive())

            profiler.put(("1", 0.001))
            flush()

            profiler.put(("2", 0.002))
            flush()

            self.assertTrue(profiler.is_alive())
            profiler.put(("3", 0.003))
            flush()
            self.assertTrue(profiler.is_alive())

            profiler.join_from("test complete")
            flush()
            self.assertFalse(profiler.is_alive())
        finally:
            if profiler.is_alive():
                profiler.join_from("test complete")
