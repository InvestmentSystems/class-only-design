import unittest

from class_only_design import core
from class_only_design import namespace
from class_only_design import constants


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
        import sys

        print(sys.version)
        print(Valid.__base__.__dict__)
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

    @unittest.skip("Not sure if this is useful")
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

        # Iteration is in reverse definition order, including overridden definitions
        self.assertListEqual(list(N2), [4, 5, 5, 3])

    def test_reserved_names(self):
        # no namespace class may use any name in constants.reserved names
        for name in constants.RESERVED_NAMES:
            # create a class that specifies name and make sure namespace raises an error
            class A:
                pass

            setattr(A, name, 5)

            # I'm using ValueError because that's what namedtuple uses if an invalid name is used
            with self.assertRaises(ValueError) as e:
                namespace.namespace(A)


class InheritanceTests(unittest.TestCase):
    """These are the same tests as for class only inheritance"""

    def test_inheritance_decorated(self):
        # test case where both classes have the @namespace decorator
        @namespace.namespace
        class X:
            x = 10

        @namespace.namespace
        class X1(X):
            y = 10
            x = 11

        self.assertEqual(X.x, 10)
        self.assertEqual(X1.x, 11)
        self.assertEqual(X1.y, 10)

    def test_inheritance_parent_decorated(self):
        # test case where only parent class has the @namespace decorator
        @namespace.namespace
        class X:
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

        @namespace.namespace
        class X1(X):
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
        @namespace.namespace
        class X:
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

    def test_base(self):
        # You can modify the undelying class if you want, using __base__. This isn't by design, but
        # this test exists to illustrate it.

        @namespace.namespace
        class X:
            x = 10

        with self.assertRaises(TypeError):
            X.x = 5
        X.__base__.x = 3
        self.assertEqual(X.x, 3)
