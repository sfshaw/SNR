from enum import Enum
from typing import Any, Dict, Optional, Tuple, Union

from snr import *
from snr.utils.dummy_endpoint.dummy_endpoint_factory import \
    DummyEndpointFactory


class MyEnum(Enum):
    a = "a"
    b = "b"
    c = "c"


Id = Tuple[MyEnum, str]
Key = Union[MyEnum, Id]


class TestNode(SNRTestCase):

    def test_lookup_proof_of_concept(self):

        d: Dict[Key, int] = {
            MyEnum.a: 1,
            (MyEnum.a, "2"): 2,
            (MyEnum.b, "3"): 3,
            MyEnum.b: 4
        }

        def get(id: Id) -> Optional[int]:
            val = d.get(id)
            if not val:
                val = d.get(id[0])
            return val

        self.assertEqual(1, get((MyEnum.a, "1")))
        self.assertEqual(2, get((MyEnum.a, "2")))
        self.assertEqual(3, get((MyEnum.b, "3")))
        self.assertEqual(4, get((MyEnum.b, "4")))
        self.assertIsNone(get((MyEnum.c, "1")))

    def test_get_task_handlers(self):

        def no_op(*args: Any) -> None:
            return None

        node = None
        try:
            node = Node("test",
                        self.get_config([
                            DummyEndpointFactory("dummy_endpoint_1", {
                                (TaskType.event, "by_type_and_name"): no_op,
                                TaskType.process_data: no_op
                            }),
                            DummyEndpointFactory("dummy_endpoint_2", {
                                TaskType.process_data: no_op
                            }),
                        ])
                        )

            handlers = node.get_task_handlers(tasks.terminate("test"))
            self.assertEqual(1, len(handlers))

            handlers = node.get_task_handlers(tasks.event("none"))
            self.assertEqual(0, len(handlers))

            handlers = node.get_task_handlers(
                Task(TaskType.process_data, "by_type"))
            self.assertEqual(2, len(handlers))

            node.set_terminate_flag("test done")
            node.terminate()

        finally:
            if node and not node.is_terminated():
                node.set_terminate_flag("test done")
                node.terminate()
                node = None
