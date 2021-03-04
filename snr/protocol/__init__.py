'''Provides interface-like Protocols used throughout the project

These Protocol definitions precede concrete implementations to describe exactly
what concrete implemetations can expect from each other and must do for each
other. Thus, croncrete implementations can rely on protocol definitions rather
than other concrete definitions. Defining protocols separate from concrete
implemetations makes new implementations easier and prevents some cyclic
dependancies. Protocols provide an outline for an implementation, like when a
professor provides instructions for an assignment.
'''

from .component_protocol import ComponentProtocol
from .config_protocol import ConfigProtocol
from .connection_protocol import ConnectionProtocol
from .context_protocol import ContextProtocol
from .datastore_protocol import DatastoreProtocol
from .endpoint_protocol import EndpointProtocol
from .factory_protocol import ComponentsByRole, FactoryProtocol
from .loop_protocol import LoopProtocol
from .multi_runner_protocol import MultiRunnerProtocol
from .node_protocol import NodeProtocol
from .profiler_protocol import ProfilerProtocol
from .runner_protocol import RunnerProtocol
