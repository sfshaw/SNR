from snr import *


class TestContext(SNRTestCase):
    def test_context_handler_no_profiler(self):
        context = Context("test_context", Settings(), None)
        result = context.profile(self.test_name, lambda arg: arg, "hello")
        self.assertEqual("hello", result)


if __name__ == '__main__':
    unittest.main()
