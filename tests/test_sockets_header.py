from snr import *
from snr.std.comms.sockets.sockets_header import *


class TestSocketsUtils(SNRTestCase):

    @pytest.mark.timeout(0.050)
    def test_sockets_utils(self) -> None:
        test_values = ["", "a", "abc", "abc_def_ghi"]
        for string in test_values:
            data = string.encode()
            size = pack_size(data)
            size2 = unpack_size(size)
            self.assertEqual(len(data), size2)


if __name__ == '__main__':
    unittest.main()
