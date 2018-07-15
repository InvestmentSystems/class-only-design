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

    def test_property(self):
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
