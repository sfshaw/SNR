from enum import Enum
from typing import Dict, Optional, Tuple, Union

from snr_core.base import *
from snr_core.datastore import Datastore
from snr_core.endpoint.node_core_factory import NodeCoreFactory
from snr_core.test.utils.dummy_endpoint import DummyEndpointFactory


class TestNode(SNRTestBase):

    def test_lookup_proof_of_concept(self):
        class Type(Enum):
            a = "a"
            b = "b"
            c = "c"
        Id = Tuple[Type, str]
        Key = Union[Type, Id]
        d: Dict[Key, int] = {
            Type.a: 1,
            (Type.a, "2"): 2,
            (Type.b, "3"): 3,
            Type.b: 4
        }

        def get(id: Id) -> Optional[int]:
            val = d.get(id)
            if not val:
                val = d.get(id[0])
            return val

        self.assertEqual(1, get((Type.a, "1")))
        self.assertEqual(2, get((Type.a, "2")))
        self.assertEqual(3, get((Type.b, "3")))
        self.assertEqual(4, get((Type.b, "4")))
        self.assertIsNone(get((Type.c, "1")))

    def test_get_task_handlers(self):
        root_context = RootContext("test")
        node = None
        try:
            node = Node(root_context,
                        "test",
                        Mode.TEST,
                        [
                            NodeCoreFactory(),
                            DummyEndpointFactory("dummy_endpoint_1", {
                                (TaskType.event, "by_type_and_name"): no_op,
                                TaskType.process_data: no_op
                            }),
                            DummyEndpointFactory("dummy_endpoint_2", {
                                TaskType.process_data: no_op
                            }),
                        ],
                        lambda n, s: Datastore(n, s),
                        )

            handlers = node.get_task_handlers(task.terminate("test"))
            self.assertEqual(1, len(handlers))

            handlers = node.get_task_handlers(task.event("none"))
            self.assertEqual(0, len(handlers))

            handlers = node.get_task_handlers(
                task.process_data("by_type"))
            self.assertEqual(2, len(handlers))

            node.set_terminate_flag("test done")
            node.terminate()

        except KeyboardInterrupt:
            pass
        finally:
            if node and not node.is_terminated.is_set():
                node.set_terminate_flag("test done")
                node.terminate()
                node = None


if __name__ == '__main__':
    unittest.main()
