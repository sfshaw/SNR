import unittest
from time import sleep
from typing import Any

from snr.utils.consumer import Consumer


class TestConsumer(unittest.TestCase):

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

        # TODO: Remove hacky sleeps

        def action(none: Any) -> None:
            pass
        SLEEP_TIME = 0.0002
        CATCH_UP_TIME = SLEEP_TIME * 2
        consumer = Consumer("test", action, SLEEP_TIME)
        sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        self.assertTrue(consumer.is_alive())
        sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        consumer.join()
        self.assertFalse(consumer.is_alive())
        sleep(CATCH_UP_TIME)
        self.assertFalse(consumer.is_alive())

    def test_consumer_put(self):

        # TODO: Remove hacky sleeps

        SLEEP_TIME = 0.0002
        CATCH_UP_TIME = SLEEP_TIME * 2

        self.num: int = 0

        def increment(n: int) -> None:
            self.num += n

        consumer = Consumer("test", increment, SLEEP_TIME)
        sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        self.assertEqual(0, self.num)
        consumer.put(0)
        sleep(CATCH_UP_TIME)
        consumer.catch_up("test")
        self.assertEqual(0, self.num)

        consumer.put(1)
        sleep(CATCH_UP_TIME)
        consumer.catch_up("test")
        self.assertEqual(1, self.num)

        consumer.put(2)
        sleep(CATCH_UP_TIME)
        consumer.catch_up("test")
        self.assertEqual(3, self.num)

        consumer.join()
        self.assertFalse(consumer.is_alive())
        self.assertEqual(3, self.num)


if __name__ == '__main__':
    unittest.main()
