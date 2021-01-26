import unittest
from sys import stdout
from typing import List

from snr_core.config import Config, Mode
from snr_core.factory.factory_base import FactoryBase


class SNRTestBase(unittest.TestCase):

    def setUp(self) -> None:
        stdout.flush()

    def get_config(self,
                   factories: List[FactoryBase],
                   mode: Mode = Mode.TEST
                   ) -> Config:
        return Config(mode, {"test": factories})
