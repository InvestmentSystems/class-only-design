import unittest

from class_only_design import core
from class_only_design import namespace


class TestNamespace(unittest.TestCase):
    def test_namespace(self):
        # a base class for classes intended to hold constants

        @namespace.namespace
        class Valid:
            a = 1
            b = 2
            c = 3

        # namespace classes are immutable
        with self.assertRaises(TypeError):
            Valid.a = 5

        # namespace classes are iterable
        self.assertListEqual(list(Valid), [1, 2, 3])

        # An inheriting class isn't iterable, but the namespace above it is
        class Child(Valid):
            d = 0

        self.assertListEqual(list(Child), [1, 2, 3])

        @namespace.namespace
        class Child(Valid):
            d = 0

        self.assertListEqual(list(Child), [0, 1, 2, 3])

    def test_constant(self):
        bad_state = 0

        @namespace.namespace
        class A:
            @core.constant
            def a(cls):
                nonlocal bad_state
                bad_state += 1
                return 5 + bad_state

        self.assertEqual(A.a, 6)
        self.assertEqual(A.a, 6)

    def test_nameof(self):
        @namespace.namespace
        class Valid:
            a_long_name = 1

        with self.assertRaises(AttributeError) as e:
            Valid.nameof.b

        # bonus: Namespace classes can tell you their attr names as strings
        self.assertEqual(Valid.nameof.a_long_name, "a_long_name")

    def test_attr_only_namespace(self):
        # TODO: a strict namespace class can't contain methods (ie, no callables)
        with self.assertRaises(TypeError):

            class Invalid:
                def method(*a, **k):
                    pass

        with self.assertRaises(TypeError):

            @namespace.namespace
            class Invalid:
                sneaky = lambda: 1

    def test_namespace_inheritance(self):
        @namespace.namespace
        class Valid:
            a = 1
            b = 2
            c = 3

        self.fail("basically, repeat the class_only inheritance tests")

    def test_namespace_iteration(self):
        class Regular:
            a = 1
            b = 2

        @namespace.namespace
        class N(Regular):
            c = 5
            d = 3
            b = 3

        # Namespace classes only iterate over namespace classes
        self.assertListEqual(list(N), [5, 3, 3])

        @namespace.namespace
        class N2(N):
            b = 4
            g = 5

        # Iteration is in definition order, including overridden definitions
        self.assertListEqual(list(N2), [5, 3, 4, 5])

    def test_sunder_attributes(self):
        # a concept borrowed from Enum, _sunder_ names begin and end with an underscore
        self.fail("todo")

    def test_reserved_names(self):
        #no namespace class may use any name in constants.reserved names
        self.fail('todo')
