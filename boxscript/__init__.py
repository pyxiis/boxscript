from boxscript.ast import Memory, Script
from boxscript.boxes import valid
from boxscript.lex import tokenize


class Interpreter:
    """The interface for running the code."""

    def __init__(self, script: str, inputs: dict[int, int] = None):
        """Creates an interpretation for a script with the specified inputs.

        Args:
            script ([type]): The script to run.
            inputs (dict[int, int], optional): A mapping of inputs to use. Defaults to
                None.
        """
        self.script = script
        self.memory = Memory
        if inputs is not None:
            for i in inputs:
                self.memory[i] = inputs[i]

    def run(self) -> None:
        """Runs the script."""
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
        else:
            print(box_error)
