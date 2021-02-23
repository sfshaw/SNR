import collections
import logging

from snr.types import *

from .consumer import Consumer
from .timer import Timer

DAEMON_THREAD = False
SLEEP_TIME_S = 0.0005
JOIN_TIMEOUT = 1

ProfilingResult = Tuple[str, float]

T = TypeVar("T")


class Profiler(Consumer[ProfilingResult]):
    def __init__(self, settings: Settings):
        if not settings.ENABLE_PROFILING:
            return None
        super().__init__("profiler",
                         self.store_task,
                         SLEEP_TIME_S,
                         True)  # TODO: Use of daemon thread is a hack
        self.settings = settings
        self.log = logging.getLogger(self.name)
        self.time_dict: Dict[str, Deque[float]] = {}
        self.moving_avg_len = settings.PROFILING_AVG_WINDOW_LEN

    def time(self,
             name: str,
             handler: Callable[[Any], T],
             *args: Any
             ) -> T:
        timer = Timer()
        result = handler(*args)
        self.store_event(name, timer.current())
        return result

    def store_event(self, task_type: str, runtime: float):
        self.put((task_type, runtime))

    def store_task(self, type_and_runtime: Tuple[str, float]):
        (task_type, runtime) = type_and_runtime
        self.log.debug("Ran %s task in %s",
                       task_type, self.format_time(runtime))
        if self.time_dict.get(task_type) is None:
            self.init_task_type(task_type)
        self.time_dict[task_type].append(runtime)
        self.log.debug("Task %s has average runtime %s",
                       task_type,
                       self.avg_time(task_type, self.time_dict[task_type]))

    def init_task_type(self, task_type: str):
        self.time_dict[task_type] = collections.deque(
            maxlen=self.moving_avg_len)

    def dump(self):
        self.log.info("Task/Loop type:\t\tAvg runtime: ")
        for k, deq in self.time_dict.items():
            self.log.info("%s:\t\t%s",
                          k, self.avg_time(k, deq))

    def avg_time(self, key: str, deque: Deque[float]) -> str:
        return self.format_time(float(sum(deque)) / float(len(deque)))

    def format_time(self, time_s: float) -> str:
        if time_s > 1:
            return "{:6.3f} s".format(time_s)
        if time_s > 0.001:
            return "{:6.3f} ms".format(time_s * 1000)
        if time_s > 0.000001:
            return "{:6.3f} us".format(time_s * 1000000)
        if time_s > 0.000000001:
            return "{:6.3f} ns".format(time_s * 1000000000)
        return "Could not format time"
