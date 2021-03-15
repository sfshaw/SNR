import dataclasses
import logging
from typing import Any, Optional

import dataclasses_json

from .names import Role
from .serializable import *

MAX_PRINTABLE_DATA_LEN = 60


DataKey = str
'''The key to get a piece of data.
'''
# TODO: Suprress inherited docstrings from str

log = logging.getLogger('Page')
log.setLevel(logging.WARNING)


@dataclasses.dataclass
class Page(dataclasses_json.DataClassJsonMixin):
    '''Basic unit of data handled by the Datastore
    '''
    key: DataKey  # The name used to lookup a page
    data: Any  # The actual data stored by a page
    origin: Role  # The node that the data came from
    created_at_s: float  # The runtime in seconds when the page was created
    process: bool = True  # If the data should be processed with task handlers

    def serialize(self) -> bytes:
        ''' Convert an instance of a Page into a JSON str
        '''
        json = self.to_json().encode()  # type: ignore

        log.debug("Page serialized to json: %s",
                  json)
        return json

    @classmethod
    def deserialize(cls, json: Optional[JsonData]) -> Optional['Page']:
        '''Attempt to convert a JSON str into a Page
        If the JSON str does not contain the information needed to construct a
        page, an error is logged and None is returned. In some cases, such as
        tests, this failure is expected.
        '''
        try:
            return Page.from_json(json)  # type: ignore
        except Exception as e:
            log = logging.getLogger('Page')
            log.error("Could not deserialize Page from json: %s, e: %s",
                      json, e)
            return None

    def __repr__(self):
        data = str(self.data)
        if len(data) > MAX_PRINTABLE_DATA_LEN:
            data = type(self.data)
        return "k: {},\t v: {},\to: {},\tt: {},\tp: {}".format(
            self.key,
            data,
            self.origin,
            self.created_at_s,
            self.process)
