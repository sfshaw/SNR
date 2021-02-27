import logging
import multiprocessing as mp

import pytest
from snr import *


class TestPipeLoop(SNRTestCase):

    def test_expector_proc(self) -> None:
        expectations: Expectations = {
            "called": 1
        }
        with MPExpector(expectations, self) as expector:
            def call():
                expector.call("called")

            proc = mp.Process(target=call)
            proc.start()
            proc.join()


if __name__ == '__main__':
    unittest.main()
