from typing import Any, Dict

from snr import *


class InputMappingEndpoint(Endpoint):

    output_data: DataKey
    mapping: Dict[str, str] = {
        "button_0": "d_pad_tap",
        "button_1": "right_stick_press",
        "button_2": "A",
        "button_3": "B",
        "button_4": "X",
        "button_5": "Y",
        "button_6": "left_shoulder",
        "button_7": "right_shoulder",
        "button_8": "left_trigger",
        "button_9": "right_trigger",
        "button_13": "left_stick_press",
        "button_15": "left_paddle",
        "button_16": "right_paddle",
        "axis_0": "left_stick_X",
        "axis_1": "left_stick_Y",
        "axis_2": "right_stick_X",
        "axis_3": "right_stick_Y",
    }

    def __init__(self,
                 factory: EndpointFactory,
                 parent: AbstractNode,
                 input_data: DataKey,
                 output_data: DataKey,
                 ) -> None:
        super().__init__(factory, parent, "controller_input_map_endpoint")
        self.output_data = output_data
        self.task_handlers = {
            (TaskType.store_page, input_data): self.map_raw_input
        }

    def map_raw_input(self, task: Task, id: TaskId) -> SomeTasks:
        page = task.val_list[0]
        assert isinstance(page, Page)
        raw_data: Dict[str, Any] = page.data
        assert isinstance(raw_data, dict)
        data: Dict[str, Any] = {}
        for key, value in raw_data.items():
            new_key = InputMappingEndpoint.mapping.get(key)
            if new_key is not None:
                data[new_key] = value
        return self.store_data_task(self.output_data, data)

    def begin(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass
