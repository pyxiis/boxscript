from lang.ast import Memory, Script
from lang.boxes import valid
from lang.lex import tokenize


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
        if not isinstance(valid(self.script), SyntaxError):
            try:
                Script(tokenize(self.script)).execute()
            except (ValueError, ZeroDivisionError):
                # printing negatives can be used as quick exit, as can division by 0
                pass
            print()
