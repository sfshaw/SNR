import os
import unittest
from typing import IO, Any

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

    def does_exist(self) -> bool:
        return os.path.exists(self.path)

    def assertExists(self):
        self.testcase.assertTrue(self.does_exist(),
                                 f"File {self.path} does not exist")

    def assertDoesNotExist(self):
        self.testcase.assertFalse(self.does_exist(),
                                  f"File {self.path} already exists")

    def __enter__(self) -> "TempFile":
        if not self.overwrite:
            self.assertDoesNotExist()
        return self

    def __exit__(self, *_: Any) -> None:
        self.assertExists()
        if self.cleanup:
            os.remove(self.path)
