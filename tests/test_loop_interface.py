from snr import *
from snr.interfaces import AbstractComponent


class NotALoop(ThreadLoop):
    def __init__(self) -> None:
        pass


class CorrectlyImplementsLoop(ThreadLoop):
    def __init__(self, factory: LoopFactory, parent: AbstractNode) -> None:
        super().__init__(factory, parent, "actually_a_loop")

    def setup(self) -> None:
        pass

    def loop(self) -> None:
        pass

    def halt(self) -> None:
        pass

    def terminate(self) -> None:
        pass


class MyLoopFac(LoopFactory):
    def __init__(self) -> None:
        super().__init__()

    def get(self, parent: AbstractNode) -> AbstractLoop:
        return CorrectlyImplementsLoop(self, parent)


class TestComponentProtocols(SNRTestCase):
    def test_abstract_loop(self) -> None:
        self.assertRaises(TypeError, lambda: NotALoop())  # type: ignore

        actually_a_loop = MyLoopFac().get(self.mock_node())
        self.assertTrue(isinstance(actually_a_loop,
                                   AbstractComponent))   # type: ignore
        self.assertTrue(isinstance(actually_a_loop,
                                   AbstractLoop))  # type: ignore
