import pytest
from snr import *
from snr.std_mods.comms.sockets_base import sockets_header


class TestSocketsUtils(SNRTestCase):

    @pytest.mark.timeout(0.050)
    def test_sockets_utils(self) -> None:
        test_values = ["", "a", "abc", "abc_def_ghi"]
        for string in test_values:
            data = string.encode()
            size = sockets_header.pack_size(data)
            size2 = sockets_header.unpack_size(size)
            self.assertEqual(len(data), size2)
