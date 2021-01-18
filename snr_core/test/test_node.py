from enum import Enum
from typing import Dict, Optional, Tuple, Union

from snr import task
from snr.config import Mode
from snr.context.root_context import RootContext
from snr.endpoint.dummy import DummyEndpointFactory
from snr.node import Node
from snr.task import TaskType
from snr.test.utils.test_base import *
from snr.utils.utils import no_op


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
        with RootContext("test", self.stdout) as root_context:
            node = None
            try:
                node = Node(root_context, "test", Mode.TEST, [
                    DummyEndpointFactory("dummy_endpoint_1", {
                        (TaskType.event, "by_type_and_name"): no_op,
                        TaskType.process_data: no_op
                    }),
                    DummyEndpointFactory("dummy_endpoint_2", {
                        TaskType.process_data: no_op
                    })])

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
                if node:
                    node.set_terminate_flag("test done")
                    node.terminate()


if __name__ == '__main__':
    unittest.main()
