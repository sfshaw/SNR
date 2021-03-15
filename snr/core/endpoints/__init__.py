'''This module defines the concrete endpoint base class and its
 constructor.
The NodeCoreEndpoint is also defined here.
'''

from .endpoint import Endpoint
from .endpoint_factory import EndpointFactory

__all__ = [
    "Endpoint",
    "EndpointFactory",
]
