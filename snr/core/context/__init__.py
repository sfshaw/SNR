'''This module contains concrete classes for the ContextProtocol.
These classes act as base classes to provide common functionality to other
classes. This functionality includes logging shortcuts and profiling wrappers.
'''

from .context import Context
from .root_context import RootContext

__all__ = ["Context", "RootContext"]
