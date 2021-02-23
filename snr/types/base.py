from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import (IO, Any, Callable, Deque, Dict, Generic, Iterable, List,
                    Optional, TextIO, Tuple, TypeVar, Union)

# JSON Serialization derivation mixin
from dataclasses_json import DataClassJsonMixin
# [Java] Interface-like definitions
from typing_extensions import Protocol, runtime_checkable
