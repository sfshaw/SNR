import threading
import time

from snr.core.base import *
from snr.core.utils.consumer import Consumer
from snr.core.utils.test_base import *
from snr.core.utils.utils import no_op

SLEEP_TIME_S = 0.00005


class TestConsumer(SNRTestCase):

    def test_increment(self):
        self.num: int = 0

        def increment(n: int) -> None:
            self.num += n

        self.assertEqual(0, self.num)
        increment(0)
        self.assertEqual(0, self.num)
        increment(1)
        self.assertEqual(1, self.num)
        increment(2)
        self.assertEqual(3, self.num)

    def test_consumer_start_join(self):
        CATCH_UP_TIME = SLEEP_TIME_S * 10
        consumer = Consumer[int]("test_start_join",
                                 no_op,
                                 SLEEP_TIME_S)

        time.sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        time.sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        consumer.join_from("test complete")
        self.assertFalse(consumer.is_alive())
        time.sleep(CATCH_UP_TIME)
        self.assertFalse(consumer.is_alive())

    def test_consumer_put(self):

        self.lock = threading.Lock()
        self.num: int = 0

        def increment(n: int) -> None:
            with self.lock:
                self.num += n

        def check(value: int) -> None:
            with self.lock:
                self.assertEqual(value, self.num)
        consumer = Consumer("test_put",
                            increment,
                            SLEEP_TIME_S)

        def flush() -> None:
            if consumer.is_alive():
                time.sleep(SLEEP_TIME_S * 10)
                consumer.flush()
                time.sleep(SLEEP_TIME_S * 10)
                consumer.flush()

        try:

            flush()
            self.assertTrue(consumer.is_alive())
            check(0)

            consumer.put(0)
            flush()
            check(0)

            consumer.put(1)
            flush()
            check(1)

            self.assertTrue(consumer.is_alive())
            consumer.put(2)
            flush()
            check(3)
            self.assertTrue(consumer.is_alive())

            consumer.join_from("test complete")
            flush()
            self.assertFalse(consumer.is_alive())
            check(3)
        finally:
            consumer.join_from("test complete")


if __name__ == '__main__':
    unittest.main()
