'''Provides interface-like Protocols used throughout the project

These Protocol definitions precede concrete implementations to describe exactly
what concrete implemetations can expect from each other and must do for each
other. Thus, croncrete implementations can rely on protocol definitions rather
than other concrete definitions. Defining protocols separate from concrete
implemetations makes new implementations easier and prevents some cyclic
dependancies. Protocols provide an outline for an implementation, like when a
professor provides instructions for an assignment.
'''

from .abstract_component import AbstractComponent
from .abstract_config import AbstractConfig
from .abstract_connection import AbstractConnection
from .abstract_context import AbstractContext
from .abstract_endpoint import AbstractEndpoint
from .abstract_factory import AbstractFactory, ComponentsByRole
from .abstract_loop import AbstractLoop
from .abstract_multi_runner import AbstractMultiRunner
from .abstract_node import AbstractNode
from .abstract_profiler import AbstractProfiler, ProfilerGetter
from .abstract_runner import AbstractRunner
from .abstract_task_queue import AbstractTaskQueue
from .timer_protocol import TimerProtocol

__all__ = [
    "AbstractComponent",
    "AbstractConfig",
    "AbstractConnection",
    "AbstractContext",
    "AbstractEndpoint",
    "ComponentsByRole",
    "AbstractFactory",
    "AbstractLoop",
    "AbstractMultiRunner",
    "AbstractNode",
    "AbstractProfiler",
    "ProfilerGetter",
    "AbstractRunner",
    "AbstractTaskQueue",
    "TimerProtocol",
]
