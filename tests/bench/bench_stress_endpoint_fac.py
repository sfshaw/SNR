import logging
import unittest
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
                 max_endpoints: int = 1000,
                 time_limit_s: float = 0.500,
                 ) -> None:
        super().__init__()
        self.max_endpoints = max_endpoints
        self.time_limit_s = time_limit_s
        self.calls = 0
        self.num_children = 0

    def get(self, parent: AbstractNode) -> Optional[Endpoint]:
        self.calls += 1
        if self.is_limited(parent):
            return None
        self.num_children += 1
        return StressorEndpoint(self,
                                parent,
                                f"stressor_endpoint_{self.num_children}")

    def is_limited(self, parent: AbstractNode) -> bool:
        return (self.num_children >= self.max_endpoints or
                (self.time_limit_s != 0 and
                 parent.get_time_s() >= self.time_limit_s))


class BenchStressEndpointFac(SNRTestCase):

    def test_stress_endpoint_init(self):
        stressor_fac = StressorEndpointFactory(max_endpoints=1,
                                               time_limit_s=0.050)
        times: List[float] = []
        node: AbstractNode = Node(
            "test",
            self.get_config([
                stressor_fac,
                TimeoutLoopFactory(seconds=0.010),
                StopwatchEndpointFactory(times,
                                         [TaskType.terminate]),
            ], Mode.DEBUG))
        node.log.setLevel(logging.WARNING)
        node.loop()
        self.assertEqual(stressor_fac.num_children, 1)
        self.assertEqual(len(times), 1)

    def test_stress_endpoint(self):
        time_target_s: float = 2.000
        stressor_fac = StressorEndpointFactory(max_endpoints=10000,
                                               time_limit_s=time_target_s)
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
        print("\nStressed with:\n",
              f"\t{stressor_fac.num_children} stressor endpoints\n",
              f"\t{stressor_fac.calls} stressor factory calls\n",
              f"\tTerminate expected at {time_target_s * 1000:.0f} ms\n",
              f"\t{times[0] * 1000:.3f} ms terminate handled\n",
              f"\t{t_s * 1000:.3f} ms total time\n",
              )
        if node.profiler:
            print(node.profiler.dump())


if __name__ == '__main__':
    unittest.main()
