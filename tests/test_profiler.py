import time
import unittest

from snr import *
from snr.core.contexts.local_profiler import LocalProfiler

SLEEP_TIME_S: float = 0.00005
CATCH_UP_TIME_S = SLEEP_TIME_S * 4


class TestProfiler(unittest.TestCase):

    def test_no_operations(self):
        profiler: AbstractProfiler = LocalProfiler()
        profiler.join_from("test_complete")
        profiler.dump()

    def test_profiler_start_join(self):
        prof: AbstractProfiler = LocalProfiler()

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(prof.is_alive())

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(prof.is_alive())

        prof.join_from("test complete")
        # LocalProfiler does not get joined/killed
        # self.assertFalse(prof.is_alive())
        # time.sleep(CATCH_UP_TIME_S)
        # self.assertFalse(prof.is_alive())

    def test_profiler_put(self):

        profiler = LocalProfiler()

        def flush() -> None:
            pass
            # if profiler.is_alive():
            #     time.sleep(CATCH_UP_TIME_S)
            #     profiler.flush()
            #     time.sleep(CATCH_UP_TIME_S)
            #     profiler.flush()

        try:
            flush()
            self.assertTrue(profiler.is_alive())

            profiler.store_task("1", 0.001)
            flush()

            profiler.store_task("2", 0.002)
            flush()

            self.assertTrue(profiler.is_alive())
            profiler.store_task("3", 0.003)
            flush()
            self.assertTrue(profiler.is_alive())

            profiler.join_from("test complete")
            flush()
            # self.assertFalse(profiler.is_alive())
        finally:
            if profiler.is_alive():
                profiler.join_from("test complete")
