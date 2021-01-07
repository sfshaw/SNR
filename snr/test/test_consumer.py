
from time import sleep

from snr.test.utils.test_base import *
from snr.utils.consumer import Consumer
from snr.utils.utils import no_op


class TestConsumer(SNRTestBase):

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
        SLEEP_TIME = 0.0002
        CATCH_UP_TIME = SLEEP_TIME * 2
        consumer = Consumer[int]("test_start_join",
                                 no_op,
                                 SLEEP_TIME,
                                 self.stdout.print)

        sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        self.assertTrue(consumer.is_alive())
        sleep(CATCH_UP_TIME)
        self.assertTrue(consumer.is_alive())

        consumer.join_from("test complete")
        self.assertFalse(consumer.is_alive())
        sleep(CATCH_UP_TIME)
        self.assertFalse(consumer.is_alive())

    def test_consumer_put(self):
        SLEEP_TIME = 0.0002

        self.num: int = 0

        def increment(n: int) -> None:
            self.num = self.num + n

        consumer = Consumer("test_put",
                            increment,
                            SLEEP_TIME,
                            self.stdout.print)
        consumer.flush()
        self.assertTrue(consumer.is_alive())

        self.assertEqual(0, self.num)
        consumer.put(0)
        consumer.flush()
        self.assertEqual(0, self.num)

        consumer.put(1)
        consumer.flush()
        self.assertEqual(1, self.num)

        self.assertTrue(consumer.is_alive())
        consumer.put(2)
        consumer.flush()
        self.assertEqual(3, self.num)
        self.assertTrue(consumer.is_alive())

        consumer.join_from("test complete")
        self.assertFalse(consumer.is_alive())
        self.assertEqual(3, self.num)


if __name__ == '__main__':
    unittest.main()
