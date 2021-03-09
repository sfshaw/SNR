import collections
from snr import *


class TestMovingAvgFilter(SNRTestCase):
    def test_filter(self):
        deque = collections.deque(maxlen=3)
        filter = MovingAvgFilter(deque)

        expectations = [
            (0.0, 0.0),
            (1.0, 0.5),
            (2.0, 1.0),
            (4.0, 7.0 / 3),
            (8.0, 14.0 / 3),
        ]
        self.assertEqual(filter.avg(), 0)
        for (val, expected_avg) in expectations:
            filter.update(val)
            self.assertEqual(filter.avg(), expected_avg)
