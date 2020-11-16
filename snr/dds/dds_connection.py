from snr.context.context import Context
from snr.dds.page import InboundStoreFn, Page
from snr.utils.utils import no_op


class DDSConnection(Context):
    def __init__(self,
                 name: str,
                 parent_context: Context,
                 inbound_store: InboundStoreFn = no_op
                 ) -> None:
        super().__init__(name, parent_context)
        self.inbound_store = inbound_store

    def send(self, data: Page) -> None:
        raise NotImplementedError

    def join(self) -> None:
        raise NotImplementedError
