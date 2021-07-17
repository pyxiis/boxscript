"""Execute code.

This module provides the necessary functions/classes to execute BoxScript.
"""

from collections import defaultdict

from boxscript.ast import Memory, Script
from boxscript.boxes import valid
from boxscript.lex import tokenize


class Interpreter:
    """The interface for running the code."""

    __slots__ = ["script", "memory"]

    def __init__(self):
        """Creates an interpreter. This class should used to execute code."""
        self.script = ""
        self.memory = Memory

    def run(self, script: str, inputs: dict[int, int] = None) -> None:
        """Runs the script.

        Args:
            script (str): The script to run.
            inputs (dict[int, int], optional): A mapping of inputs to use. Defaults to
                None.
        """
        self.script = script

        if inputs is not None:
            for i in inputs:
                self.memory[i] = inputs[i]

        box_error = valid(self.script)
        if not isinstance(box_error, SyntaxError):
            try:
                Script(tokenize(self.script)).execute()
                print()
            except (ValueError, ZeroDivisionError):
                # printing negatives can be used as quick exit, as can division by 0
                print()
            except SyntaxError as e:
                print(e)
            except RecursionError:
                # this does not matter, just stop the code
                print("maximum recursion depth exceeded")
        else:
            print(box_error)

        self.memory = defaultdict(int)
        self.script = ""
