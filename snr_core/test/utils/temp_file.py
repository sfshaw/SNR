import os
import unittest
from typing import IO, Any


class TempFile:
    def __init__(self,
                 testcase: unittest.TestCase,
                 path: str,
                 overwrite: bool = False,
                 cleanup: bool = True
                 ) -> None:
        self.testcase = testcase
        self.overwrite = overwrite
        self.cleanup = cleanup
        self.path = path

    def open(self) -> IO[Any]:
        return open(self.path, 'x')

    def assertExists(self):
        self.testcase.assertTrue(os.path.exists(self.path),
                                 f"File {self.path} does not exist")

    def __enter__(self):
        if not self.overwrite:
            self.testcase.assertFalse(os.path.exists(self.path),
                                      f"File {self.path} already exists")
        return self

    def __exit__(self, *_: Any) -> None:
        self.assertExists()
        if self.cleanup:
            os.remove(self.path)
