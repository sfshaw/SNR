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

        consumer = Consumer("test", action, 0.001)
        # self.assertFalse(consumer.is_alive())
        # sleep(0.05)
        # self.assertFalse(consumer.is_alive())

        # consumer.start()
        self.assertTrue(consumer.is_alive())
        sleep(0.05)
        self.assertTrue(consumer.is_alive())

        consumer.join()
        self.assertFalse(consumer.is_alive())
        sleep(0.05)
        self.assertFalse(consumer.is_alive())

    def test_consumer_put(self):

        # TODO: Remove hacky sleeps

        self.num: int = 0

        def increment(n: int) -> None:
            self.num += n

        consumer = Consumer("test", increment, 0.001)

        # Stay dead
        # self.assertFalse(consumer.is_alive())
        # sleep(0.05)
        # self.assertFalse(consumer.is_alive())

        # Stay alive
        # consumer.start()
        self.assertTrue(consumer.is_alive())
        sleep(0.05)
        self.assertTrue(consumer.is_alive())

        self.assertEqual(0, self.num)
        consumer.put(0)
        sleep(0.05)
        consumer.catch_up()
        self.assertEqual(0, self.num)

        consumer.put(1)
        sleep(0.05)
        consumer.catch_up()
        self.assertEqual(1, self.num)

        consumer.put(2)
        sleep(0.05)
        consumer.catch_up()
        self.assertEqual(3, self.num)

        consumer.join()
        self.assertFalse(consumer.is_alive())
        self.assertEqual(3, self.num)


if __name__ == '__main__':
    unittest.main()
