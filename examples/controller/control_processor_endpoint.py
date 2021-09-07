from typing import Any, List, Dict

from snr import *


class ControlProcessorEndpoint(Endpoint):

    input_data: DataKey
    watch_buttons: List[str] = [
        "d_pad_tap",
        "right_stick_press",
        "A",
        "B",
        "X",
        "Y",
        "left_shoulder",
        "right_shoulder",
        "left_trigger",
        "right_trigger",
        "left_stick_press",
        "left_paddle",
        "right_paddle",
    ]

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 input_data: DataKey,
                 ) -> None:
        super().__init__(factory, parent, "input_processor_endpoint")
        self.input_data = input_data
        self.task_handlers = {
            (TaskType.store_page, input_data): self.process_input
        }

    def process_input(self, task: Task, id: TaskId) -> SomeTasks:
        page = task.val_list[0]
        assert isinstance(page, Page)
        prev_data: Dict[str, Any] = self.get_data(  # type: ignore
            self.input_data+"_prev")
        if prev_data is None:
            self.info("No previous input data")
            return None
        data: Dict[str, Any] = page.data
        assert isinstance(prev_data, dict) and isinstance(data, dict)
        events: List[Task] = []
        for key, value in data.items():
            prev = prev_data[key]
            if value == 0 and prev == 1:
                events.append(tasks.event("button_released", [key]))
            if value == 1 and prev == 0:
                events.append(tasks.event("button_pressed", [key]))
        return events

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
