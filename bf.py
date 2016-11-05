#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function

import sys

"""
Instructions:
.   print to stdout
,   read from stdin
+   increment current value
-   decrement current value
<   Move pointer left
>   Move pointer right
[   Move to corresponding ']' if current value equal to zero. Otherwise,
    continue to next Instruction.
]   Destination if value from corresponding '[' was zero. Move back to
    corresponding '[' when reached.


Things to check for later:
Does the [ just jump to the next ] or the next corresponding ]. IE, will
I need a stack counter for [ and ]. For example, for  "[[]]", does the first
[ jump to the first or second ]. For now, I am implementing it with the
second option with the stack counter.

Are the values supposed to be signed or unsigned integers/longs/whatever.
"""


PRINT_STDOUT = "."
READ_STDIN = ","
INCREMENT_VALUE = "+"
DECREMENT_VALUE = "-"
DECREMENT_POINTER = "<"
INCREMENT_POINTER = ">"
CONDITION_CHECK = "["
CONDITION_END = "]"


class InputStream(object):
    """This class exists because I do not remember how to convert a string
    to a file stream."""

    def pop_char(self):
        raise NotImplementedError


class IOStream(InputStream):
    def __init__(self, io_stream):
        self.__stream = io_stream

    def pop_char(self):
        return self.__stream.read(1)


class StdinStream(IOStream):
    def __init__(self):
        super(StdinStream, self).__init__(sys.stdin)


class StringStream(InputStream):
    def __init__(self, s):
        self.__s = s

    def pop_char(self):
        if not self.__s:
            raise RuntimeError("Attempting to pop off empty string stream.")
        c = self.__s[0]
        self.__s = self.__s[1:]
        return c


class Interpretter(object):
    def __init__(self, stack_size=30000, starting_stack=None,
                 return_str=False, input_stream=None, pointer_start=0):
        if starting_stack:
            self.__stack_size = len(starting_stack)
            self.__stack = starting_stack
        else:
            self.__stack_size = stack_size
            self.__stack = [0]*stack_size

        self.__input_stream = input_stream or StdinStream()

        if self.__stack_size <= 0:
            raise RuntimeError("The stack size must not be zero or negative.")

        if pointer_start >= self.__stack_size:
            raise RuntimeError("The pointer cannot start at a value greater than or equal to the length of the stack.")

        self.__pointer = pointer_start
        self.__pc = 0  # Program counter
        self.__return_str = return_str
        self.__output_buffer = ""

    def run(self, query):
        """Interpret some code."""
        while self.__pc < len(query):
            c = query[self.__pc]

            if c == PRINT_STDOUT:
                self.print_stdout()
            elif c == READ_STDIN:
                self.read_stdin()
            elif c == INCREMENT_VALUE:
                self.increment_value()
            elif c == DECREMENT_VALUE:
                self.decrement_value()
            elif c == DECREMENT_POINTER:
                self.decrement_pointer()
            elif c == INCREMENT_POINTER:
                self.increment_pointer()
            elif c == CONDITION_CHECK:
                self.condition_check(query)
                # Continue because this manually adjusts the pc
                continue
            elif c == CONDITION_END:
                self.condition_end(query)
                # Continue because this manually adjusts the pc
                continue
            # Ignore all other characters

            self.__pc += 1

        if self.__return_str:
            return self.__output_buffer

    def print_stdout(self):
        """Print the char of the current value to stdout."""
        c = chr(self.__stack[self.__pointer])
        if self.__return_str:
            self.__output_buffer += c
        else:
            print(c)

    def read_stdin(self):
        """Read byte value from stdin into current value."""
        self.__stack[self.__pointer] = ord(self.__input_stream.pop_char())

    def increment_value(self):
        """Increment the value of the current pointer."""
        self.__stack[self.__pointer] += 1

    def decrement_value(self):
        """Decrement the value of the current pointer."""
        self.__stack[self.__pointer] -= 1

    def decrement_pointer(self):
        """
        Decrement the pointer value (move it to the left).
        Circle to end of stack if less than 0.
        """
        self.__pointer -= 1
        if self.__pointer < 0:
            self.__pointer = self.__stack_size - 1

    def increment_pointer(self):
        """
        Increment the pointer value (move it to the right).
        Circle to start of stack if more than stack size.
        """
        self.__pointer += 1
        if self.__pointer >= self.__stack_size:
            self.__pointer = 0

    def condition_check(self, query):
        """
        Move to corresponding condition end if current value is zero.
        Otherwise, continue to next instruction.
        This method manually adjusts the pc to the desired index.
        """
        if self.__stack[self.__pointer]:
            self.__pc += 1
        else:
            # Advance stream
            counter = 1
            while counter:
                while query[self.__pc] != CONDITION_END:
                    self.__pc += 1

                    if self.__pc >= len(query):
                        raise RuntimeError("Unbalanced number of conditional brackets. PC surpassed length of code.")

                    if query[self.__pc] == CONDITION_CHECK:
                        counter += 1

                # Move to instruction after the ]
                self.__pc += 1
                counter -= 1

                if self.__pc >= len(query) and counter:
                    raise RuntimeError("Unbalanced number of conditional brackets. PC surpassed length of code.")



    def condition_end(self, query):
        """
        Landing condition from previous condition check for when current
        value is zero. Move back to previous condition check when reached.
        This method manually adjusts the pc to the desired index.
        """
        counter = 1
        while counter:
            self.__pc -= 1
            if self.__pc < 0:
                raise RuntimeError("Unbalanced number of conditional brackets. PC decremented below zero.")

            if query[self.__pc] == CONDITION_END:
                counter += 1
            elif query[self.__pc] == CONDITION_CHECK:
                # Stay on [ if found
                counter -= 1

    def stack(self):
        return self.__stack

    def pointer(self):
        return self.__pointer


def run(code, **kwargs):
    """Spawn an instance of the Interpretter and run through it."""
    intrp = Interpretter(**kwargs)
    out = intrp.run(code)
    return out


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Brainfuck Interpretter")
    parser.add_argument("filename", help="Brainfuck file.")
    return parser.parse_args()


def main():
    args = get_args()
    with open(args.filename, "r") as f:
        run(f.read())


if __name__ == "__main__":
    main()

