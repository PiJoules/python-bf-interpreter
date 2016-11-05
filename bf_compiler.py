#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
More understandable language that compiles into BF.

Setting an integer:
set [num]  # Sets current value to [num]
set_zero  # Sets current value to 0

Moving the pointer:
move [num]  # Increments the pointer [num] times. If [num] is negative,
            # the pointer is decremented instead.

Incrementing current value:
"""

# Commands
SET = "set"
SET_ZERO = "set_zero"
MOVE = "move"


class Compiler(object):
    def __init__(self):
        pass

    def parse_instruction(self, instr):
        parts = instr.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == SET:
            return self.parse_set(*args)
        elif cmd == SET_ZERO:
            return self.parse_set_zero(*args)
        elif cmd == MOVE:
            return self.parse_move(*args)
        else:
            raise RuntimeError("Unknown command '{}'".format(cmd))

    def compile(self, code):
        output = ""
        for line in code.split("\n"):
            output += self.parse_instruction(line)
        return output

    def parse_set(self, *args):
        if not len(args) == 1:
            raise RuntimeError("Only 1 argument for MOVE is expected.")

        if not self.is_int(args[0]):
            raise RuntimeError("can only set whole numbers.")

        return self.set_int(int(args[0]))

    def parse_set_zero(self, *args):
        if len(args):
            raise RuntimeError("SET_ZERO expects no arguments.")
        return self.set_zero()

    def parse_move(self, *args):
        if not len(args) == 1:
            raise RuntimeError("Only 1 argument for MOVE is expected.")

        if not self.is_int(args[0]):
            raise RuntimeError("can only MOVE by whole numbers.")

        return self.move_int(int(args[0]))

    def is_int(self, s):
        if s[0] == "-":
            return s[1:].isdigit()
        return s.isdigit()

    def set_zero(self):
        """Sets the current value to zero."""
        return "[-]"

    def set_int(self, i):
        """First set the current value to zero, then increment."""
        out = self.set_zero()
        if i > 0:
            out += "+"*i
        elif i < 0:
            out += "-"*abs(i)
        return out

    def move_int(self, i):
        if i > 0:
            return ">"*i
        elif i < 0:
            return "<"*abs(i)
        return ""


def main():
    compiler = Compiler()
    code = """set 3
    set_zero
    set -4
    move 4
    move -2"""
    output = compiler.compile(code)
    print(output)


if __name__ == "__main__":
    main()

