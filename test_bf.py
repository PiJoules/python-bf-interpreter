#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bf import run, StringStream, Interpretter

import unittest


class TestBF(unittest.TestCase):
    """More integration tests really."""

    def test_pointer_start(self):
        self.assertRaises(RuntimeError, Interpretter, stack_size=10, pointer_start=10)

    def test_zero_stack_size(self):
        self.assertRaises(RuntimeError, Interpretter, stack_size=0)

    def test_print_stdout(self):
        stack = [ord("a")]
        code = "."
        output = run(code, starting_stack=stack, return_str=True)
        self.assertEqual("a", output)

    def test_read_stdin(self):
        code = ",."
        output = run(code, return_str=True, input_stream=StringStream("a"))
        self.assertEqual("a", output)

    def test_increment_value(self):
        code = "+"
        intrp = Interpretter()
        intrp.run(code)
        self.assertEqual(intrp.stack()[0], 1)

    def test_decrement_value(self):
        code = "-"
        intrp = Interpretter()
        intrp.run(code)
        self.assertEqual(intrp.stack()[0], -1)

    def test_decrement_pointer(self):
        code = "<"
        intrp = Interpretter(pointer_start=1)
        intrp.run(code)
        self.assertEqual(intrp.pointer(), 0)

    def test_decrement_pointer_circular(self):
        """Test that the pointer cycles to end of the stack."""
        code = "<"
        intrp = Interpretter(stack_size=10)
        intrp.run(code)
        self.assertEqual(intrp.pointer(), 9)

    def test_increment_pointer(self):
        code = ">"
        intrp = Interpretter()
        intrp.run(code)
        self.assertEqual(intrp.pointer(), 1)

    def test_decrement_pointer_circular(self):
        """Test that the pointer cycles to start of the stack."""
        code = ">"
        intrp = Interpretter(stack_size=10, pointer_start=9)
        intrp.run(code)
        self.assertEqual(intrp.pointer(), 0)

    def test_condition(self):
        code = "[-]."
        intrp = Interpretter(return_str=True, starting_stack=[10])
        output = intrp.run(code)
        self.assertEqual(output, "\0")
        self.assertEqual(intrp.stack(), [0])

    def test_condition_bounds(self):
        self.assertRaises(RuntimeError, run, "[[]")
        self.assertRaises(RuntimeError, run, "[]]")


if __name__ == "__main__":
    unittest.main()
