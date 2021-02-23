from snr import *
from snr.core.node import Node
from snr.core.utils.utils import no_op
from snr.types.task import task_process_data


class TestNode(SNRTestCase):

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
        node = None
        try:
            node = Node(self.root_context,
                        "test",
                        Mode.TEST,
                        [
                            DummyEndpointFactory("dummy_endpoint_1", {
                                (TaskType.event, "by_type_and_name"): no_op,
                                TaskType.process_data: no_op
                            }),
                            DummyEndpointFactory("dummy_endpoint_2", {
                                TaskType.process_data: no_op
                            }),
                        ])

            handlers = node.get_task_handlers(task_terminate("test"))
            self.assertEqual(1, len(handlers))

            handlers = node.get_task_handlers(task_event("none"))
            self.assertEqual(0, len(handlers))

            handlers = node.get_task_handlers(
                task_process_data("by_type"))
            self.assertEqual(2, len(handlers))

            node.set_terminate_flag("test done")
            node.terminate()

        except KeyboardInterrupt:
            pass
        finally:
            if node and not node.is_terminated():
                node.set_terminate_flag("test done")
                node.terminate()
                node = None


if __name__ == '__main__':
    unittest.main()
