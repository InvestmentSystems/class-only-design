import unittest
import gc

from class_only_design import util


class TestUtil(unittest.TestCase):
    def test_keygetter(self):
        class A:
            a = 5
            long_name = "tim"

        A.nameof = util.KeyGetter(A)

        self.assertEqual(A.nameof.a, "a")
        self.assertEqual(A.nameof.long_name, "long_name")
        self.assertIn("a", dir(A.nameof))
        self.assertIn("long_name", dir(A.nameof))

        with self.assertRaises(AttributeError) as e:
            A.nameof.doesntexist

    def test_weakref(self):
        # keygetter doesn't keep its class alive
        class A:
            a = 5

        A.nameof = util.KeyGetter(A)

        n = A.nameof
        del A
        gc.collect()
        with self.assertRaises(ReferenceError):
            n.a
