"""Parse a tokenization.

This module provides the necessary functions to construct the AST for BoxScript.
"""

import collections
import itertools
from typing import Optional

from lang.lex import Atom, Node, Token

Memory = collections.defaultdict(lambda: 0)
STDOut = ""
c = 0


def shunting_yard(tokens: list[Token]) -> list[Token]:
    """Generates the RPN representation of the given list of Tokens.

    This function should not be used with certain Tokens, such as list assignment or
    output. These should be taken care of with special cases.

    Args:
        tokens (list[Token]): An input list of numerical Tokens.

    Returns:
        list[Token]: The Tokens in RPN order
    """

    output = []
    stack = []
    for token in tokens:
        if token.type is Atom.NUM:
            output.append(token)
        elif token.type in [Atom.MEM, Atom.NOT]:
            while any(
                op in map(lambda e: e.type, stack) for op in [Atom.MEM, Atom.NOT]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token.type in [Atom.L_SHIFT, Atom.R_SHIFT]:
            while any(
                op in map(lambda e: e.type, stack)
                for op in [Atom.L_SHIFT, Atom.R_SHIFT, Atom.MEM, Atom.NOT]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token.type is Atom.AND:
            while any(
                op in map(lambda e: e.type, stack)
                for op in [Atom.AND, Atom.L_SHIFT, Atom.R_SHIFT, Atom.MEM, Atom.NOT]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token.type is Atom.XOR:
            while any(
                op in map(lambda e: e.type, stack)
                for op in [
                    Atom.XOR,
                    Atom.AND,
                    Atom.L_SHIFT,
                    Atom.R_SHIFT,
                    Atom.MEM,
                    Atom.NOT,
                ]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token.type is Atom.OR:
            while any(
                op in map(lambda e: e.type, stack)
                for op in [
                    Atom.OR,
                    Atom.XOR,
                    Atom.AND,
                    Atom.L_SHIFT,
                    Atom.R_SHIFT,
                    Atom.MEM,
                    Atom.NOT,
                ]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token.type is Atom.L_PAREN:
            stack.append(token)
        elif token.type is Atom.R_PAREN:
            while stack[-1].type is not Atom.L_PAREN:
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output


class Nil(Node):
    """A Node which does nothing."""

    def execute(self) -> int:
        """Returns 1.

        Returns:
            int: 1.
        """
        return 1


class Container(Node):
    """A node which contains semi-parsed code, such as other Containers, as children."""

    __slots__ = ["children"]

    def __init__(self, children: list[Node] = None):
        """Create a new Container.

        Args:
            children (list, optional): The children of the Container. Defaults to None.
        """
        if children is None:
            children = []
        self.children = children

    def execute(self) -> int:
        """Executes all children.

        Returns:
            int: The outcome of the last execution.
        """
        r = 0
        for child in self.children:
            r = child.execute()
        return r


class Block(Container):
    """A class representing a "block" of code."""

    def execute(self) -> int:
        """Executes all children.

        Returns:
            int: The outcome of the last execution.
        """
        r = 0
        for child in self.children:
            if isinstance(child, Line):
                child.parse()
                if isinstance(child.children[0], Nil):
                    continue
            r = child.execute()
        return r


class IfBlock(Block):
    """A class for denoting conditional blocks of code."""


class ExecBlock(Block):
    """A class for denoting executable blocks of code."""


class Box(Container):
    """A class for denoting a single "box" of code.

    This is a loop in other languages. Sort of.
    """

    def execute(self) -> int:
        """Executes all children.

        Returns:
            int: 0 if a conditional fails, 1 otherwise. Infinite loops will give an
                error because Python does not support infinite loops. Essentially,
                any box which has a conditional will return 0.
        """
        conditional = any(isinstance(child, IfBlock) for child in self.children)
        if conditional:
            for child in self.children:
                value = child.execute()
                if isinstance(child, IfBlock) and not value:
                    return 0
            self.execute()
        else:
            for child in self.children:
                child.execute()
        return 1


class Expression(Container):
    """A class for denoting and evaluating an RPN expression."""

    def execute(self) -> int:
        """Evaluates the RPN expression.

        Returns:
            int: The value of the expression.
        """
        stack = [0]

        for child in self.children:
            if child.type is Atom.NUM:
                stack.append(child.value)
            elif child.type is Atom.MEM:
                stack.append(Memory[stack.pop()])
            elif child.type is Atom.L_SHIFT:
                stack.append(stack.pop() << stack.pop())
            elif child.type is Atom.R_SHIFT:
                stack.append(stack.pop() >> stack.pop())
            elif child.type is Atom.AND:
                stack.append(stack.pop() & stack.pop())
            elif child.type is Atom.OR:
                stack.append(stack.pop() | stack.pop())
            elif child.type is Atom.XOR:
                stack.append(stack.pop() ^ stack.pop())

        return stack.pop()


class Line(Container):
    """A class for a line of code.

    Note:
        A Line cannot contain any other Containers. In a sense, Lines are the
        "molecules" of BoxScript.
    """

    __slots__ = ["line_number", "parsed", "output"]
    lineno = 0

    def __init__(self, children: list[Node] = None):
        """Create a new Line.

        Args:
            children (list, optional): The children of the Line. Defaults to None.
        """
        super().__init__(children)
        self.parsed = False
        self.line_number = Line.lineno
        self.output = False

        Line.lineno += 1

    def parse(self) -> None:
        """Parses the line.

        Note:
            This method should only be called once. Nothing happens when it is called
            more than once, but that call would therefore be redundant.
        """
        if self.parsed:
            return

        if self.children:
            self.output = self.children[0].type is Atom.OUT
            if self.output:
                self.children = self.children[1:]

        split_assign = [
            list(group)
            for key, group in itertools.groupby(
                self.children, lambda tok: tok.type is Atom.ASSIGN
            )
            if not key
        ]

        if len(split_assign) > 1:
            loc = Expression(shunting_yard(split_assign[0]))
            value = Expression(shunting_yard(split_assign[1]))

            class Assign(Container):
                def execute(self) -> int:
                    value = self.children[1].execute()
                    loc = self.children[0].execute()
                    Memory[loc] = value
                    return value

            assignment = Assign(children=[loc, value])

            self.children = [assignment]
        elif len(split_assign) == 1:
            value = Expression(shunting_yard(split_assign[0]))
            self.children = [value]
        else:
            self.children = [Nil()]

        self.parsed = True

    def valid(self) -> Optional[SyntaxError]:
        """Checks whether the line is valid.

        Returns:
            Optional[SyntaxError]: The syntax error, if any.
        """
        # test parentheses
        parens = 0
        for token in self.children:
            if token.type == Token.L_PAREN:
                parens += 1
            elif token.type == Token.R_PAREN:
                parens -= 1
            if parens < 0:
                return SyntaxError(f"Unmatched parentheses at line {self.line_number}")
        if parens:
            return SyntaxError(f"Unmatched parentheses at line {self.line_number}")

        split_assign = [
            list(group)
            for key, group in itertools.groupby(
                self.children, lambda tok: tok.type is Atom.ASSIGN
            )
            if not key
        ]

        # test assignments
        if len(split_assign) > 2:
            return SyntaxError(
                f"Too many assignment operations on line {self.line_number}"
            )

        # test outputs
        out_count = len(filter(lambda child: child.type is Atom.OUTPUT, self.children))
        if out_count > 1:
            return SyntaxError(f"Too many output operations on line {self.line_number}")
        elif out_count == 1:
            if self.children[0].type is not Atom.OUTPUT:
                return SyntaxError(
                    f"Output operation must be at the beginning of line "
                    f"{self.line_number}"
                )

    def execute(self) -> int:
        """Executes all children

        Returns:
            int: The outcome of the execution.
        """
        if self.children:
            r = self.children[0].execute()
        else:
            r = 0

        if self.output:
            print(f"output: {chr(r)}")

        # x = str(Memory)
        # if len(x) < 100:
        #     print(f"{self.line_number}: {Memory}")

        return r


class Script(Container):
    """A class for the Container which contains all code.

    This class is needed because the script must be parsed into Containers, which is
        done in the __init__.
    """

    def __init__(self, children: list[Token] = None):
        """Creates the Container which contains all Containers.

        Note:
            This also parses the script into a list of Containers, which are then
            assigned as children.

        Args:
            children (list[Token], optional): All tokens belonging to a script. Defaults
                to None.
        """
        if children is None:
            children = []

        super().__init__()
        box_stack = [Container()]

        for child in children:
            if child.type in [Atom.BOX_START, Atom.EXEC_START, Atom.IF_START]:
                if child.type is Atom.BOX_START:
                    b = Box()
                    box_stack.pop()  # remove newline from the stack
                elif child.type is Atom.EXEC_START:
                    b = ExecBlock()
                elif child.type is Atom.IF_START:
                    b = IfBlock()
                box_stack[-1].children.append(b)
                box_stack.append(box_stack[-1].children[-1])
            elif child.type in [Atom.BOX_END, Atom.EXEC_END, Atom.IF_END]:
                if child.type in [Atom.EXEC_END, Atom.IF_END]:
                    box_stack.pop()  # remove newline from stack
                box_stack.pop()
            elif child.type is Atom.NEWLINE:
                if isinstance(box_stack[-1], Line):
                    box_stack.pop()
                box_stack[-1].children.append(Line())
                box_stack.append(box_stack[-1].children[-1])
            else:
                box_stack[-1].children.append(child)

        self.children = [
            child for child in box_stack[0].children if not isinstance(child, Line)
        ]
