from typing import Any

from snr_core.endpoint.endpoint import Endpoint


class Factory:
    def __init__(self, name: str) -> None:
        self.name = name

    def get(self, parent: Any) -> Endpoint:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def __repr__(self):
        return self.name
