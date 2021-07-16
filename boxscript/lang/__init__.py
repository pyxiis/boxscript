from lang.ast import Memory, Script
from lang.boxes import valid
from lang.lex import tokenize


class Interpreter:
    def __init__(self, script, inputs: dict[int, int] = None):
        self.script = script
        self.memory = Memory
        if inputs is not None:
            for i in inputs:
                self.memory[i] = inputs[i]

    def run(self):
        if not isinstance(valid(self.script), SyntaxError):
            try:
                Script(tokenize(self.script)).execute()
            except ValueError:
                # printing negatives can be used as quick exit
                pass
            print()
