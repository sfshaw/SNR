
from typing import Any, Callable

import snr
from snr import (AbstractNode, Endpoint, EndpointFactory, LoopFactory,
                 ThreadLoop, tasks)
from snr.prelude import *


class RadarSensorLoop(ThreadLoop):

    fuel: int
    altitude: float
    velocity: float

    def __init__(self,
                 factory: LoopFactory,
                 parent: AbstractNode,
                 fuel: int,
                 ) -> None:
        super().__init__(factory, parent,
                         "radar_sensor_endpoint",
                         max_tick_rate_hz=1)
        self.fuel = fuel
        self.altitude = 50.0
        self.velocity = 0.0

    def setup(self) -> None:
        self.store_data("thruster_data", 0)

    def loop(self) -> None:
        page = self.get_page("thruster_data")
        assert isinstance(page, Page) and isinstance(page.data, int)
        thruster_value: int = page.data

        self.velocity += -9.8 + thruster_value * 0.1
        self.altitude += self.velocity

        if self.altitude <= 0:
            # *Attempted Landing*
            if self.velocity < -1.0:
                raise Exception("High velocity impact")
            else:
                self.schedule(tasks.terminate("Landed Safely"))
                self.set_terminate_flag()

        self.store_data("radar_data", (self.altitude, self.velocity))

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class RadarSensorLoopFactory(LoopFactory):

    initial_fuel: int

    def __init__(self, initial_fuel: int) -> None:
        super().__init__()
        self.initial_fuel = initial_fuel

    def get(self, parent: AbstractNode) -> RadarSensorLoop:
        return RadarSensorLoop(self, parent, self.initial_fuel)


class QLearningControllerEndpoint(Endpoint):

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 q_function: Callable[[Any, int], float],
                 ) -> None:
        super().__init__(factory, parent, "q_learning_controler")
        self.task_handlers = {
            (TaskType.store_page, "radar_data"): self.set_throttle,
        }
        self.q_function = q_function
        self.actions = [0, 1, 2, 3, ]

    def set_throttle(self, t: Task, key: TaskId) -> SomeTasks:
        assert (len(t.val_list) > 0 and
                len(t.val_list[0]) == 2 and
                isinstance(t.val_list[0][0], int) and
                isinstance(t.val_list[0][0], float) and
                isinstance(t.val_list[0][0], float))
        radar_data = t.val_list[0]
        value = self.policy(radar_data)
        return tasks.store_data("thruster_data", value)

    def policy(self, data: Any) -> int:
        return max(self.actions, key=lambda a: self.q_function(data, a))


class QLearningControllerEndpointFactory(EndpointFactory):
    def __init__(self) -> None:
        super().__init__()

    def get(self, parent: AbstractNode) -> QLearningControllerEndpoint:
        return QLearningControllerEndpoint(self, parent)


config = snr.Config(factories={
    "lunar_module": [
        RadarSensorLoopFactory(initial_fuel=100),
        QLearningControllerEndpointFactory(),
    ],
})


def main():
    snr.SynchronousRunner("lunar_module", config).run()


if __name__ == "__main__":
    main()
