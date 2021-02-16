from snr.snr_protocol import *
from snr.snr_types import *
from snr.snr_types.task import task_process_data

from .context.context import Context
from .utils.timer import Timer

SLEEP_TIME_S = 0.0001

DataDict = Dict[DataKey, Page]


class Datastore(Context):
    def __init__(self,
                 parent: ContextProtocol,
                 task_scheduler: TaskScheduler,
                 timer: Timer,
                 ) -> None:
        super().__init__("datastore", parent)
        self.timer = timer
        self.parent = parent
        self.data_dict: DataDict = {}
        self.schedule_task = task_scheduler

        self.info("Datastore initialized")

    def page(self, key: str, value: Any, process: bool = True) -> Page:
        created_at = self.timer.current()
        return Page(key, value, self.parent.name, created_at, process)

    def get_data(self, key: str) -> Optional[Any]:
        page = self.get_page(key)
        if page:
            return page.data
        return None

    def get_page(self, key: str) -> Optional[Page]:
        return self.data_dict.get(key)

    def synchronous_store(self, page: Page) -> None:
        self.write(page)

    def dump_data(self) -> None:
        for page in self.data_dict.values():
            self.dump("%s", page)

    def write(self, page: Page) -> None:
        self.data_dict[page.key] = page
        self.dbg("Stored Page(%s)", page.key)
        if page.process:
            t = task_process_data(page.key)
            self.schedule_task(t)
