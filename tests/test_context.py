from typing import TypeVar

from snr import *


class TestContext(SNRTestCase):
    def test_context_handler_no_profiler(self):

        T = TypeVar('T')

        def no_op(input: T) -> T:
            return input

        context: AbstractContext = Context(
            "test_context", Settings(), None, Timer())
        result = context.profile(self.test_name, no_op, "hello")
        self.assertEqual("hello", result)
