from typing_extensions import Protocol, runtime_checkable
from dataclasses_json.mm import JsonData
from dataclasses_json import DataClassJsonMixin
from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import (IO, Any, Callable, Deque, Dict, Generic, Iterable, List,
                    Optional, TextIO, Tuple, TypeVar, Union)

ReloadTargets = Union[ModuleType,
                      List[ModuleType]]

# JSON Serialization
# [Java] Interface-like definitions
