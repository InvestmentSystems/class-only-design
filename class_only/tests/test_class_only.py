#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `class_only` package."""


import unittest

from class_only import api


class TestClassOnly(unittest.TestCase):
    """Tests for `class_only` package."""

    def test_class_only(self):
        """Test something."""

        @api.class_only
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

            @api.class_only
            class Invalid:
                def __new__(*a, **k):
                    pass

        with self.assertRaises(TypeError):

            @api.class_only
            class Invalid:
                def __init__(*a, **k):
                    pass

    def test_wraps(self):
        # The class is wrapped correctly, such that attributes are preserved
        @api.class_only
        class Test:
            pass

        self.assertEqual(Test.__name__, "Test")

    def test_property(self):
        class A:
            @property
            def a(self):
                return 5

            # class myprop

        a = A()
        self.fail()
