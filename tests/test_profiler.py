import time

from snr.core.base import *
from snr.core.utils.profiler import Profiler
from snr.core.utils.test_base import *

SLEEP_TIME_S = 0.00005


class TestProfiler(unittest.TestCase):

    def test_no_operations(self):
        profiler: ProfilerProtocol = Profiler(Settings())
        profiler.join_from("test_complete")
        profiler.dump()

    def test_profiler_start_join(self):
        CATCH_UP_TIME = SLEEP_TIME_S * 10
        profiler: ProfilerProtocol = Profiler(Settings())

        time.sleep(CATCH_UP_TIME)
        self.assertTrue(profiler.is_alive())

        time.sleep(CATCH_UP_TIME)
        self.assertTrue(profiler.is_alive())

        profiler.join_from("test complete")
        self.assertFalse(profiler.is_alive())
        time.sleep(CATCH_UP_TIME)
        self.assertFalse(profiler.is_alive())

    def test_consumer_put(self):

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


if __name__ == '__main__':
    unittest.main()
