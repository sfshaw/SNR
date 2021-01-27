
from snr_core.modes import Components, ComponentsByRole, Mode
from snr_core.endpoint.node_core_factory import NodeCoreFactory

from snr_core.context.root_context import RootContext


class Config:
    def __init__(self,
                 mode: Mode,
                 factories: ComponentsByRole = {}
                 ) -> None:
        self.mode = mode
        self.factories = factories
        if not factories:
            raise Exception("No factories provided")

    def get(self, role: str) -> Components:
        factories = self.factories[role]
        factories.append(NodeCoreFactory())
        return factories

    def root_context(self,
                     name: str
                     ) -> RootContext:
        return RootContext(name)
