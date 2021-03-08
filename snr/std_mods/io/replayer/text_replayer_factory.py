from snr.core import *
from . import text_replayer


class TextReplayerFactory(LoopFactory):
    def __init__(self,
                 input_filename: str,
                 output_data_name: str,
                 exit: bool = False
                 ) -> None:
        super().__init__(text_replayer)
        self.input_filename = input_filename
        self.output_data_name = output_data_name
        self.exit = exit

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return text_replayer.TextReplayer(self,
                                          parent,
                                          self.input_filename,
                                          self.output_data_name,
                                          self.exit)

    def __repr__(self):
        return f"TextReplayerFactory({self.output_data_name})"
