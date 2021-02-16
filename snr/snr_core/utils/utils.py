"""Various helper utilities used throughout the code
Attempts to document propper usage of such functions
"""

from snr.snr_types.base import *


def no_op(*args: Any) -> None:
    pass


def init_dict(keys: List[str], val: Any) -> Dict[str, Any]:
    d = {}
    for k in keys:
        d[k] = val
    return d
