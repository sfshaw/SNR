import logging
from typing import List, Optional

from snr import *

STRESS_TASK_NAME: TaskName = "stress"


class StressorEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 name: ComponentName,
                 ) -> None:
        super().__init__(factory, parent, name)
        self.task_handlers = {
            (TaskType.event, STRESS_TASK_NAME): self.replicate,
        }

    def replicate(self, task: Task, key: TaskId) -> SomeTasks:
        return tasks.add_component(self.factory)

    def begin(self) -> None:
        self.schedule(tasks.event(STRESS_TASK_NAME))

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class StressorEndpointFactory(EndpointFactory):
    def __init__(self,
                 max_endpoints: int = 10000,
                 time_limit_s: float = 0,
                 ) -> None:
        super().__init__()
        self.max_endpoints = max_endpoints
        self.time_limit_s = time_limit_s
        self.num_children = 0

    def get(self, parent: AbstractNode) -> Optional[Endpoint]:
        self.num_children += 1
        if (self.num_children > self.max_endpoints and
                (self.time_limit_s == 0.0 or
                 parent.get_time_s() < self.time_limit_s)):
            return None
        return StressorEndpoint(self,
                                parent,
                                f"stressor_endpoint_{self.num_children}")


class TestStress(SNRTestCase):

    def test_stress_endpoint(self):
        time_target_s: float = 0.100
        stressor_fac = StressorEndpointFactory(max_endpoints=100,
                                               time_limit_s=0.100)
        times: List[float] = []
        timer = Timer()
        node: AbstractNode = Node(
            "test",
            self.get_config([
                stressor_fac,
                TimeoutLoopFactory(
                    seconds=time_target_s),
                StopwatchEndpointFactory(times,
                                         [TaskType.terminate]),
            ], Mode.DEBUG))
        node.log.setLevel(logging.WARNING)
        node.loop()
        t_s = timer.current_s()
        print("\n".join([
            "Stressed with:",
            f"\t{stressor_fac.num_children} stressor endpoints",
            f"\t{times[0] * 1000:.3f} ms terminate triggered",
            f"\t{t_s * 1000:.3f} ms total time",
        ]))
        if node.profiler:
            print(node.profiler.dump())
