"""Various helper utilities used throughout the code
Attempts to document propper usage of such functions
"""

import sys
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union


def print_usage() -> None:
    """Prints a Unix style uasge message on how to start the program
    """
    print(f"usage: {sys.executable} main.py [robot | topside]")


def no_op(*args: Any) -> None:
    pass


def init_dict(keys: List[str], val: Any) -> Dict[str, Any]:
    d = {}
    for k in keys:
        d[k] = val
    return d
