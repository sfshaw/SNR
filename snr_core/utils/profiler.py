from collections import deque
from typing import Any, Callable, Deque, Dict, Tuple

from snr_core.settings import Settings
from snr_core.utils.consumer import Consumer
from snr_core.utils.debug.channels import *
from snr_core.utils.debug.debugger import Debugger
from snr_core.utils.timer import Timer

DAEMON_THREAD = False
SLEEP_TIME_S = 0.01
JOIN_TIMEOUT = 1

ProfilingResult = Tuple[str, float]


class Profiler(Consumer[ProfilingResult]):
    def __init__(self, debugger: Debugger, settings: Settings):
        if not settings.ENABLE_PROFILING:
            return None
        super().__init__("profiler",
                         self.store_task,
                         SLEEP_TIME_S,
                         debugger.stdout.print)
        self.debugger = debugger
        self.settings = settings
        self.time_dict: Dict[str, Deque[float]] = {}
        self.moving_avg_len = settings.PROFILING_AVG_WINDOW_LEN

    def time(self, name: str, handler: Callable[[Any], Any], args: Any) -> Any:
        timer = Timer()
        result = handler(args)
        self.log_task(name, timer.current())
        return result

    def log_task(self, task_type: str, runtime: float):
        self.put((task_type, runtime))

    def store_task(self, type_and_runtime: Tuple[str, float]):
        (task_type, runtime) = type_and_runtime
        self.debugger.debug("profiling_task", DEBUG_CHANNEL,
                            "Ran {} task in {}",
                            [task_type, self.format_time(runtime)])
        if self.time_dict.get(task_type) is None:
            self.init_task_type(task_type)
        self.time_dict[task_type].append(runtime)
        self.debugger.debug("profiling_avg",
                            PROFILING_CHANNEL,
                            "Task {} has average runtime {}",
                            [task_type, self.avg_time(task_type)])

    def init_task_type(self, task_type: str):
        self.time_dict[task_type] = deque(maxlen=self.moving_avg_len)

    def dump(self):
        self.debugger.debug("profiling", DUMP_CHANNEL,
                            "Task/Loop type:\t\tAvg runtime: ")
        for k in self.time_dict.keys():
            self.debugger.debug("profiling_dump", DUMP_CHANNEL, "{}:\t\t{}", [
                                k, self.avg_time(k)])

    def avg_time(self, key: str) -> str:
        q = self.time_dict[key]
        return self.format_time(sum(q) / len(q))

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