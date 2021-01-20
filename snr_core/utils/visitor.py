

from typing import Generic, List, TypeVar, Union
import unittest


CONSUMER_THREAD_NAME_SUFFIX = "_consumer_thread"

DAEMON_THREADS: bool = False

T = TypeVar('T')
U = TypeVar('U')


class Visitor(Generic[T, U]):
    def __init__(self) -> None:
        pass

    def visit(self, visitee: T) -> U:
        raise NotImplementedError


MyType = Union[str, int, float, None]


class MyTypeVisitor(Visitor[MyType, int]):
    def visit(self, visitee: MyType) -> int:
        if isinstance(visitee, str):
            return self.visit_str(visitee)
        elif isinstance(visitee, int):
            return self.visit_int(visitee)
        elif isinstance(visitee, float):
            return self.visit_float(visitee)
        elif visitee is None:
            return self.visit_none()
        else:
            raise TypeError

    def visit_str(self, visitee: str) -> int:
        raise NotImplementedError

    def visit_int(self, visitee: int) -> int:
        raise NotImplementedError

    def visit_float(self, visitee: float) -> int:
        raise NotImplementedError

    def visit_none(self) -> int:
        raise NotImplementedError


class MyVisitor(MyTypeVisitor):

    def visit_str(self, visitee: str) -> int:
        return len(visitee)

    def visit_int(self, visitee: int) -> int:
        return visitee

    def visit_float(self, visitee: float) -> int:
        return int(visitee * 2)

    def visit_none(self) -> int:
        return 0


class VisitorTest(unittest.TestCase):

    def setUp(self):
        self.v: MyTypeVisitor = MyVisitor()

    def test_str(self):
        self.assertEqual(0, self.v.visit(""))
        self.assertEqual(1, self.v.visit("1"))
        self.assertEqual(2, self.v.visit("tu"))

    def test_int(self):
        values = [-1000, -1, 0, 1, 2, 13, 24, 5000000]
        for i in values:
            self.assertEqual(i, self.v.visit(i))

    def test_float(self):
        self.assertEqual(1, self.v.visit(0.5))
        self.assertEqual(-2, self.v.visit(-1.2))
        self.assertEqual(0, self.v.visit(0.0))
        self.assertEqual(3, self.v.visit(1.6))
        self.assertEqual(20000, self.v.visit(10000.0))

    def test_none(self):
        self.assertEqual(0, self.v.visit(None))

    def test_all(self):
        values: List[MyType] = ["", "22", "tre",
                                -4, 5, 0,
                                0.0, 0.0000001, 29.0,
                                None, None, None]
        expected: List[int] = [0, 2, 3,
                               -4, 5, 0,
                               0, 0, 58,
                               0, 0, 0]
        actual = [self.v.visit(item) for item in values]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
