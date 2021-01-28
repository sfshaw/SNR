from typing import Optional, TextIO

from snr_core.base import *

NAME_PREFIX = "raw_replayer_"


class RawReader(Context):
    def __init__(self,
                 parent: Context,
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

    def read(self) -> Optional[str]:
        if self.file:
            try:
                raw_line = self.file.readline()
                self.dbg(f"Read line: {raw_line}")
                line = raw_line.rstrip()
                if len(line) > 0:
                    return line
            except Exception as e:
                self.err("Error reading file: %s", e)
                return None
        return None

    def close(self) -> None:
        if self.file:
            self.file.close()


class RawDataReplayer(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent: NodeProtocol,
                 filename: str,
                 data_name: str,
                 exit_when_done: bool
                 ) -> None:
        super().__init__(factory,
                         parent,
                         NAME_PREFIX + data_name)
        self.data_name = data_name
        self.reader = RawReader(self, "raw_reader", filename)
        self.done: bool = False
        self.exit_when_done = exit_when_done
        self.next_page: Optional[Page] = None

    def loop_handler(self) -> None:
        if not self.done:
            line = self.reader.read()
            if line:
                self.parent.store_data(self.data_name, line)
            elif not self.done:
                self.dbg("Reader Done")
                self.done = True
                if self.exit_when_done:
                    self.dbg("Reader scheduling terminate task")
                    self.parent.schedule(task.terminate("replayer_done"))

    def terminate(self) -> None:
        self.reader.close()
