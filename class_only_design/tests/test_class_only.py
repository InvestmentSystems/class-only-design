#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `class_only` package."""


import unittest

from class_only_design import core


class TestClassOnly(unittest.TestCase):
    """Tests for `class_only` package."""

    def test_class_only(self):
        """Test something."""

        @core.class_only
        class ValidTest:
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

            @core.class_only
            class Invalid:
                def __new__(*a, **k):
                    pass

        with self.assertRaises(TypeError):

            @core.class_only
            class Invalid:
                def __init__(*a, **k):
                    pass

    def test_wraps(self):
        # The class is wrapped correctly, such that attributes are preserved
        @core.class_only
        class Test:
            pass

        self.assertEqual(Test.__name__, "Test")

    def test_constant(self):
        bad_state = 0

        class A:
            @core.constant
            def a(cls):
                nonlocal bad_state
                bad_state += 1
                return 5 + bad_state

        a = A()
        self.assertEqual(A.a, 6)
        self.assertEqual(A.a, 6)
        self.assertEqual(a.a, 6)

    def test_inheritance_decorated(self):
        #test case where both classes have the @class_only decorator
        @core.class_only
        class X:
            x = 10

        @core.class_only
        class X1(X):
            y = 10
            x = 11

        self.assertEqual(X.x, 10)
        self.assertEqual(X1.x, 11)
        self.assertEqual(X1.y, 10)

    def test_inheritance_parent_decorated(self):
        #test case where only parent class has the @class_only decorator
        @core.class_only
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
        #test case where only child class has the @class_only decorator
        class X:
            x = 10
            y = 10

        @core.class_only
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
        # if a class only class is used as a mixin, what should happen?
        @core.class_only
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

        #I think class_only should propagate
        for cls in X3, X4:
            for attr in 'xyz':
                with self.assertRaises(TypeError):
                    setattr(cls, attr, 1234)

        self.assertEqual(X3.x, 1)
        self.assertEqual(X4.y, 2)

    def test_base(self):
        # You can modify the undelying class if you want, using __base__. This isn't by design, but
        # this test exists to illustrate it.

        @core.class_only
        class X:
            x = 10

        with self.assertRaises(TypeError):
            X.x = 5
        X.__base__.x = 3
        self.assertEqual(X.x, 3)
