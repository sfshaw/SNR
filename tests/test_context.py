from snr import *


class TestContext(SNRTestCase):
    def test_context_handler_no_profiler(self):

        def no_op(arg: str) -> str:
            return arg

        context = Context("test_context", self.root_context, profiler=None)
        result = context.profile(self.test_name, no_op, "hello")
        self.assertEqual("hello", result)


if __name__ == '__main__':
    unittest.main()
