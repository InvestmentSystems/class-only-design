import unittest
import sys

from class_only_design import Namespace
from class_only_design import constant
from class_only_design import constants
from class_only_design import autoname

iterable_compare = list
# In python < 3.6, classes aren't ordered
if sys.version_info < (3, 6, 0):
    iterable_compare = set


class TestNamespace(unittest.TestCase):
    def test_namespace(self):
        # a base class for classes intended to hold constants

        class Valid(Namespace):
            a = 1
            b = 2
            c = 3

        # namespace classes are immutable
        with self.assertRaises(TypeError):
            Valid.a = 5
        with self.assertRaises(TypeError):
            Valid.x = 5

        # namespace classes can't be instantiated
        with self.assertRaises(TypeError):
            Valid()

        # namespace classes are iterable
        self.assertSequenceEqual(iterable_compare(Valid), iterable_compare([1, 2, 3]))

        # Inheriting from an NS class keeps the iteration.
        class Child(Valid):
            d = 0

        self.assertSequenceEqual(
            iterable_compare(Child), iterable_compare([0, 1, 2, 3])
        )

        class Child(Valid):
            d = 0

        self.assertSequenceEqual(
            iterable_compare(Child), iterable_compare([0, 1, 2, 3])
        )

    def test_constant(self):
        bad_state = 0

        class A(Namespace):
            @constant
            def a(cls):
                nonlocal bad_state
                bad_state += 1
                return 5 + bad_state

        self.assertEqual(A.a, 6)
        self.assertEqual(A.a, 6)

    def test_nameof(self):
        class Valid(Namespace):
            a_long_name = 1

        with self.assertRaises(AttributeError) as e:
            Valid.nameof.b

        # Namespace classes can tell you their attr names as strings
        self.assertEqual(Valid.nameof.a_long_name, "a_long_name")

    def test_namespace_iteration(self):
        class Regular:
            a = 1
            b = 2

        class N(Regular, Namespace):
            c = 5
            d = 3
            b = 3

        # Namespace classes only iterate over namespace classes
        self.assertSequenceEqual(iterable_compare(N), iterable_compare([5, 3, 3]))

        class N2(N):
            b = 4
            g = 5

        # Iteration is in reverse definition order, including overridden definitions
        self.assertSequenceEqual(iterable_compare(N2), iterable_compare([4, 5, 5, 3]))

    def test_reserved_names(self):
        # no namespace class may use any name in constants.reserved names
        for name in constants.RESERVED_NAMES:
            # create a class that specifies name and make sure namespace raises an error
            class A:
                pass

            setattr(A, name, 5)

            # I'm using ValueError because that's what namedtuple uses if an invalid name is used
            with self.assertRaises(ValueError, msg=name) as e:
                class ns(A, Namespace):
                    pass


class InheritanceTests(unittest.TestCase):
    """These are the same tests as for class only inheritance"""

    def test_inheritance_decorated(self):
        # test case where both classes have the @namespace decorator
        class X(Namespace):
            x = 10

        class X1(X, Namespace):
            y = 10
            x = 11

        self.assertEqual(X.x, 10)
        self.assertEqual(X1.x, 11)
        self.assertEqual(X1.y, 10)

    def test_inheritance_parent_decorated(self):
        # test case where only parent class has the @namespace decorator
        class X(Namespace):
            x = 10

        class X1(X):
            y = 10

        # once class only, always class only
        self.assertEqual(X.x, 10)
        self.assertEqual(X1.y, 10)
        self.assertEqual(X1.x, 10)

        with self.assertRaises(TypeError):
            X1.y = 5
        with self.assertRaises(TypeError):
            X1.a = 5
        with self.assertRaises(TypeError):
            X1.x = 5

    def test_inheritance_child_decorated(self):
        # test case where only child class has the @namespace decorator
        class X:
            x = 10
            y = 10

        class X1(X, Namespace):
            y = 10

        self.assertEqual(X.x, 10)
        self.assertEqual(X1.x, 10)

        # in this case, modifying the parent is allowed, of course
        X.x = 5
        self.assertEqual(X.x, 5)
        # But it also changes inherited attributes on the child...
        self.assertEqual(X1.x, 5)

        # Explicitly overridden attributes are not changed
        X.y = 5
        self.assertEqual(X.y, 5)
        self.assertEqual(X1.y, 10)

        with self.assertRaises(TypeError):
            X1.y = 5

    def test_multiple_inheritance(self):
        # if a namespace class is used as a mixin, what should happen?
        class X(Namespace):
            x = 10

        class X1:
            y = 10

        class X3(X, X1):
            x = 1
            y = 1

        class X4(X1, X):
            x = 2
            y = 2

        # I think class_only should propagate
        for cls in X3, X4:
            for attr in "xyz":
                with self.assertRaises(TypeError):
                    setattr(cls, attr, 1234)

        self.assertEqual(X3.x, 1)
        self.assertEqual(X4.y, 2)

    def test_auto_name(self):
        class A(Namespace):
            attr = autoname
            other = autoname

        self.assertEqual(A.attr, 'attr')
        self.assertEqual(A.other, 'other')
        self.assertEqual(A.nameof.attr, 'attr')
