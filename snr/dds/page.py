from typing import Any, Callable

MAX_PRINTABLE_DATA_LEN = 60


class Page:
    def __init__(self,
                 key: str,
                 data: Any,
                 origin: str,
                 created_at: float,
                 process: bool = True):
        self.key = key
        self.data = data
        self.origin = origin
        self.created_at = created_at
        self.process = process

    def __repr__(self):
        data = str(self.data)
        if len(data) > MAX_PRINTABLE_DATA_LEN:
            data = type(self.data)
        return "k: {},\t v: {},\to: {},\tt: {},\tp: {}".format(
            self.key,
            data,
            self.origin,
            self.created_at,
            self.process)


InboundStoreFn = Callable[[Page], None]
