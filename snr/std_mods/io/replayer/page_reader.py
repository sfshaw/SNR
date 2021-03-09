from typing import Any, Optional, TextIO

from snr.core import *
from snr.protocol import *
from snr.type_defs import *


class PageReader(Context):

    def __init__(self,
                 parent: ContextProtocol,
                 name: str,
                 filename: str,
                 ) -> None:
        super().__init__(name, parent.settings, parent.profiler)

        self.filename = filename
        self.file: Optional[TextIO] = None
        try:
            self.file = open(self.filename)
            self.dbg(f"File {self.filename} opened")
        except Exception as e:
            self.err(f"Error opening file: {e}")
            self.close()

    def read(self) -> Optional[Page]:
        if self.file:
            try:
                raw_line = self.file.readline()
                self.dbg(f"Read line: {raw_line}")
                line = raw_line.rstrip()
                if line:
                    return Page.deserialize(line)
            except Exception as e:
                self.warn("Error reading file: %s", e)
                return None
        return None

    def close(self) -> None:
        if self.file:
            self.file.close()

    def __enter__(self) -> "PageReader":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
