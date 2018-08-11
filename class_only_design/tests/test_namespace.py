import unittest

from class_only_design import core
from class_only_design import namespace


class TestClassOnly(unittest.TestCase):
    def test_namespace(self):
        # a base class for classes intended to hold constants

        class Valid(namespace.Namespace):
            a = 1
            b = 2
            c = 3

        # namespace classes are immutable
        with self.assertRaises(TypeError):
            Valid.a = 5

        # namespace classes are iterable
        self.assertListEqual(list(Valid), [1, 2, 3])

        # bonus: Namespace classes can tell you their attr names as strings
        self.assertEqual(Valid.nameof.a, "a")

    def test_attr_only_namespace(self):
        # TODO: a strict namespace class can't contain methods (ie, no callables)
        with self.assertRaises(TypeError):

            class Invalid:
                def method(*a, **k):
                    pass

        with self.assertRaises(TypeError):

            @core.namespace
            class Invalid:
                sneaky = lambda: 1

    def test_namespace_inheritance(self):
        @core.namespace
        class Valid:
            a = 1
            b = 2
            c = 3

        self.fail("basically, repeat the class_only inheritance tests")

    def test_namespace_iteration(self):

        class Regular:
            a = 1
            b = 2

        @core.namespace
        class N(regular):
            c = 5
            d = 3
            b = 3

        # Namespace classes only iterate over namespace classes
        self.assertListEqual(list(N), [5, 3, 2])

        @core.namespace
        class N2(N):
            b = 4
            g = 5

        # Iteration is in definition order, including overridden definitions
        self.assertListEqual(list(N2), [5, 3, 4, 5])
