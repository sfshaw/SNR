import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

from dataclasses_json import DataClassJsonMixin

MAX_PRINTABLE_DATA_LEN = 60


DataKey = str


@dataclass
class Page(DataClassJsonMixin):
    key: DataKey
    data: Any
    origin: str
    created_at: float
    process: bool = True

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

    def serialize(self) -> str:
        return self.to_json()

    @classmethod
    def deserialize(cls, json: str) -> Optional["Page"]:
        try:
            return Page.from_json(json)
        except Exception as e:
            log = logging.getLogger("Page")
            log.error("Could not deserialize Page from json: %s, e: %s",
                      json, e)
            return None


InboundStoreFn = Callable[[Page], None]
