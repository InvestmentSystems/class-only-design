#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `class_only` package."""


import unittest

from class_only_design import ClassOnly
from class_only_design import constant


class TestClassOnly(unittest.TestCase):
    """Tests for `class_only` package."""

    def test_class_only(self):
        """Test something."""

        class ValidTest(ClassOnly):
            CONSTANT = 5

            @classmethod
            def method(cls, arg):
                return arg

            @staticmethod
            def static(arg):
                return arg

            def regular(arg):
                # functionally equivalent to staticmethod. Disallow?
                return arg

        with self.assertRaises(TypeError):
            ValidTest()

        with self.assertRaises(TypeError):
            ValidTest.CONSTANT = 6

        self.assertEqual(ValidTest.method(123), 123)
        self.assertEqual(ValidTest.static(1), 1)
        self.assertEqual(ValidTest.regular(3), 3)

    def test_load_errors(self):
        # Class only classes can't specify __new__ or __init__
        with self.assertRaises(TypeError):

            class Invalid(ClassOnly):
                def __new__(*a, **k):
                    pass

        with self.assertRaises(TypeError):

            class Invalid(ClassOnly):
                def __init__(*a, **k):
                    pass

    def test_constant(self):
        bad_state = 0

        class A(ClassOnly):
            @constant
            def a(cls):
                nonlocal bad_state
                bad_state += 1
                return 5 + bad_state

        self.assertEqual(A.a, 6)
        self.assertEqual(A.a, 6)

        with self.assertRaises(TypeError):
            A.a = ""

    def test_constant_no_use_without_class_only(self):
        # constant cannot prevent setting on classes, because __set__ isn't called for
        # classes. For this reason, we disallow using constant with non class_only
        # classes.

        # In python3.11, ANY exception in __set_name__ result in RuntimeError.
        with self.assertRaises((TypeError, RuntimeError)):

            class Class:
                @constant
                def class_name(cls):
                    return cls.__name__

    def test_constant_inheritance(self):

        class A(ClassOnly):

            @constant
            def name(cls):
                return cls.__name__

        class B(A):
            pass

        class C(A):
            pass

        assert A.name == "A"
        assert B.name == "B"
        assert C.name == "C"

    def test_inheritance_decorated(self):
        # test case where both classes have the @class_only decorator
        class X(ClassOnly):
            x = 10

        class X1(X):
            y = 10
            x = 11

        self.assertEqual(X.x, 10)
        self.assertEqual(X1.x, 11)
        self.assertEqual(X1.y, 10)

    def test_inheritance_parent_decorated(self):
        # test case where only parent class has the @class_only decorator
        class X(ClassOnly):
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
        # test case where only child class has the @class_only decorator
        class X:
            x = 10
            y = 10

        class X1(X, ClassOnly):
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
        # if a class only class is used as a mixin, what should happen?
        class X(ClassOnly):
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

    def test_class_only_subclasses_can_accept_kwargs(self) -> None:

        class MyClass(ClassOnly):
            @classmethod
            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__()

                assert kwargs == dict(kwarg1=1, kwarg2=2)

        class MySubclass(MyClass, kwarg1=1, kwarg2=2):
            pass

    def test_class_only_immediate_subclass_accepts_no_kwargs(self) -> None:
        with self.assertRaises(TypeError):

            class InvalidKwargPassedToClassOnlySubclass(ClassOnly, kwarg1=1):
                pass

    def test_class_only_immediate_subclass_cannot_forward_kwargs(self) -> None:
        class MyClass(ClassOnly):
            @classmethod
            def __init_subclass__(cls, **kwargs):
                assert kwargs == dict(kwarg1=1, kwarg2=2)

                with self.assertRaises(TypeError):
                    super().__init_subclass__(**kwargs)

        class MySubclass(MyClass, kwarg1=1, kwarg2=2):
            pass
