from snr.core import *
from snr.prelude import *

from . import replayer_loop


class ReplayerLoopFactory(LoopFactory):
    def __init__(self,
                 input_filename: str,
                 exit: bool = False
                 ) -> None:
        super().__init__(replayer_loop)
        self.input_filename = input_filename
        self.exit = exit

    def get(self, parent: AbstractNode) -> AbstractLoop:
        return replayer_loop.ReplayerLoop(self,
                                          parent,
                                          self.input_filename,
                                          self.exit)
