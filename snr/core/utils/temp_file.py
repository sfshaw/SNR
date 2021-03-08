import os
from typing import Any, IO
import unittest

from snr.type_defs import *

TEMP_PATH = "temp/"


class TempFile:
    def __init__(self,
                 testcase: unittest.TestCase,
                 filename: str,
                 overwrite: bool = False,
                 cleanup: bool = True
                 ) -> None:
        self.testcase = testcase
        self.overwrite = overwrite
        self.cleanup = cleanup
        self.path = TEMP_PATH + filename
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)

    def open(self) -> IO[Any]:
        return open(self.path, 'w')

    def assertExists(self):
        self.testcase.assertTrue(os.path.exists(self.path),
                                 f"File {self.path} does not exist")

    def __enter__(self) -> "TempFile":
        if not self.overwrite:
            self.testcase.assertFalse(os.path.exists(self.path),
                                      f"File {self.path} already exists")
        return self

    def __exit__(self, *_: Any) -> None:
        self.assertExists()
        if self.cleanup:
            os.remove(self.path)
