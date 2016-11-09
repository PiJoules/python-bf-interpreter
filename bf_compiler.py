#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from bf import run

"""
More understandable language that compiles into BF.

Setting an integer:
set [num]  # Sets current value to [num]
set_zero  # Sets current value to 0

Moving the pointer:
move [num]  # Increments the pointer [num] times. If [num] is negative,
            # the pointer is decremented instead.

Incrementing current value: TODO

Setting a string:
set_str [string]

Whatever follows after the space after the command is
what will be in the string. Quotes are not necessary.
The line ends on a newline.
This function advances the stack pointer to the index after the last character
in the string.
TODO: Implement character escaping.


Printing a string:
print

This function prints up to the first null character (0).
This function advances the stack pointer to the character after the ending
null terminator.

Iteration/looping:
while  # go to instruction after corresponding end
end

"""

# Commands
SET = "set"
SET_ZERO = "set_zero"
MOVE = "move"
SET_STR = "set_str"
PRINT = "print"
WHILE = "while"
END = "end"


class Compiler(object):
    def __init__(self):
        pass

    def parse_instruction(self, instr):
        parts = instr.split(" ")
        cmd = parts[0]
        args = parts[1:]

        if cmd == SET:
            return self.parse_set(*args)
        elif cmd == SET_ZERO:
            return self.parse_set_zero(*args)
        elif cmd == MOVE:
            return self.parse_move(*args)
        elif cmd == SET_STR:
            return self.parse_set_str(*args)
        elif cmd == PRINT:
            return self.parse_print(*args)
        else:
            raise RuntimeError("Unknown command '{}'".format(cmd))

    def compile(self, code):
        output = ""
        for line in code.split("\n"):
            output += self.parse_instruction(line.strip())
        return output

    def parse_set(self, *args):
        if not len(args) == 1:
            raise RuntimeError("Only 1 argument for MOVE is expected.")

        if not self.is_int(args[0]):
            raise RuntimeError("can only set whole numbers.")

        return self.set_int(int(args[0]))

    def parse_set_zero(self, *args):
        if args:
            raise RuntimeError("SET_ZERO expects no arguments.")
        return self.set_zero()

    def parse_move(self, *args):
        if not len(args) == 1:
            raise RuntimeError("Only 1 argument for MOVE is expected.")

        if not self.is_int(args[0]):
            raise RuntimeError("can only MOVE by whole numbers.")

        return self.move_int(int(args[0]))

    def parse_set_str(self, *args):
        if not args:
            raise RuntimeError("Expected at least 1 argument for SET_STR.")

        out = ""
        for arg in args:
            for c in arg:
                out += self.set_int(ord(c)) + self.move_int(1)
        return out

    def parse_print(self, *args):
        if args:
            raise RuntimeError("PRINT expects no arguments.")
        return "[.>]"

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


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Compiles psudo-language into brainfuck.")
    parser.add_argument("filename", help="File to compile into BF.")
    parser.add_argument("-i", "--Interpret", help="Interpret after compiling.")
    return parser.parse_args()


def main():
    compiler = Compiler()
    code = """set 3
    set_zero
    set -4
    move 4
    move -2
    set_str abc
    move -3
    print"""
    output = compiler.compile(code)
    print(output)
    run(output)


if __name__ == "__main__":
    main()

