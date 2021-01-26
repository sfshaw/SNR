from snr_core.loop.loop_factory import LoopBase, LoopFactory
from snr_core.node import Node
from snr_std.io.replayer import replayer


class ReplayerFactory(LoopFactory):
    def __init__(self,
                 input_filename: str,
                 exit: bool = False
                 ) -> None:
        super().__init__("Replayer Factory")
        self.input_filename = input_filename
        self.exit = exit

    def get(self, parent: Node) -> LoopBase:
        return replayer.Replayer(self,
                                 parent,
                                 self.input_filename,
                                 self.exit)
