from snr.utils.utils import no_op
from snr.context.stdout_consumer import StdOutConsumer


ONE_HUNDRED_MICROSECONDS = 0.0001


class SilentStdOut(StdOutConsumer):
    def __init__(self, parent_name: str) -> None:
        super().__init__(parent_name,
                         no_op,
                         no_op)
