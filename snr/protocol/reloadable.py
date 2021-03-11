'''The `Reloadable` protocol separates the expected behavior for an
 implementation of the ComponentProtocol to avoid cyclic imports.
'''

from snr.type_defs import *
from typing_extensions import Protocol, runtime_checkable

from .component_protocol import ComponentProtocol
from .factory_protocol import FactoryProtocol


@runtime_checkable
class Reloadable(Protocol):
    '''Protocol implemented by `Endpoint`s and Loops so their factories may
     reload the Python module that define them and then create new instances.
    '''
    factory: FactoryProtocol
    '''The factory that knows how to reload the aComponent`'s Python module
    '''

    def halt(self) -> None:
        '''Clean up method for endpoints and loops. Should leave the factory
        in a state to restart the component after reloading.
        '''
        ...

    def reload(self) -> FactoryProtocol:
        '''Concrete implementation of reload for all `Reloadable`s
        '''
        self.factory.reload()
        self.halt()
        return self.factory
