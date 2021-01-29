from typing import Optional, TextIO

from snr.snr_core.base import *

NAME_PREFIX = "raw_replayer_"


class PageReader(Context):
    def __init__(self,
                 parent: SettingsProvider,
                 name: str,
                 filename: str,
                 ) -> None:
        super().__init__(name, parent)

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


class Replayer(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 filename: str,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "replayer")
        self.reader = PageReader(self, "raw_reader", filename)
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def loop_handler(self) -> None:
        if not self.done:
            page = self.reader.read()
            if page:
                self.parent.store_page(page)
            elif not self.done:
                self.dbg("Reader Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Reader scheduling terminate task")
                    self.parent.schedule(task.terminate("replayer_done"))

    def terminate(self) -> None:
        self.reader.close()
