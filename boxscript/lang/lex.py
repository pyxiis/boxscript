"""Tokenize an input string.

This module provides the necessary classes and functions to tokenize BoxScript code.

Note:
    The tokenization done in this module is not designed to support syntax
    highlighting. Many parts of the code (e.g. comments) are simply ignored, rather than
    tokenized as a comment. It is impossible to reconstitute the original code from the
    tokenization.

    Syntax highlighting should be done using regex.
"""

from enum import Enum
import functools
import re

__all__ = ["Atom", "Node", "Token", "tokenize"]


Atom = Enum(
    "Atom",
    [
        "NOT",
        "AND",
        "XOR",
        "OR",
        "L_SHIFT",
        "R_SHIFT",
        "MEM",
        "NUM",
        "OUT",
        "IN",
        "L_PAREN",
        "R_PAREN",
        "BOX_START",
        "BOX_END",
        "IF_START",
        "IF_END",
        "EXEC_START",
        "EXEC_END",
        "NEWLINE",
        "ASSIGN",
    ],
)


class Node:
    """A node of BoxScript code. This class is used for type hints."""

    def execute(self) -> int:
        """Executes all children.

        Raises:
            NotImplementedError: This function is not modified in subclass.

        Returns:
            int: The outcome of the execution.
        """
        raise NotImplementedError


class Token(Node):
    """A BoxScript Token which represents a single "atom" of code."""

    __slots__ = ["type", "value"]

    def __init__(self, type: Atom, value: int = None):
        """Creates a BoxScript token.

        Args:
            type (Atom): The type of token
            value (int, optional):  The value of the token—only exists for NUM tokens.
                Defaults to None.
        """
        self.type = type
        self.value = value
    
    def execute(self):
        # print(self.type)
        pass


def tokenize(code: str) -> list[Token]:
    """Creates a list of tokens from BS code.

    Args:
        code (str): The input code.

    Returns:
        list[Token]: The list of BS tokens.
    """
    tokens = []

    while code:
        match = functools.partial(re.match, string=code)

        if m := match(r"[▄▀]+"):
            if len(m.group()) > 1:
                value = (
                    int(
                        "".join(
                            map(
                                lambda digit: {"▄": "0", "▀": "1"}[digit], m.group()[1:]
                            )
                        ),
                        2,
                    )
                    * (2 * (m.group()[0] == "▀") - 1)
                )
                tokens.append(Token(Atom.NUM, value))
            else:
                tokens.append(Token(Atom.NUM, 0))
            code = code[len(m.group()) :]
        elif m := (match(r"[╔╚╠]═*[╗╝╣]") or match(r"[║][^\n]*[║]")):
            code = code[len(m.group()) :]
        else:
            if code[0] in "┌└├┞┟┏┗┣┢┡":
                if code[0] in "┌┏":
                    tokens.append(Token(Atom.BOX_START))

                    if code[0] == "┌":
                        tokens.append(Token(Atom.EXEC_START))
                    else:
                        tokens.append(Token(Atom.IF_START))

                elif code[0] in "├┞┟┣┢┡":
                    if code[0] in "├┟┢":
                        tokens.append(Token(Atom.EXEC_END))
                    else:
                        tokens.append(Token(Atom.IF_END))

                    if code[0] in "├┞┡":
                        tokens.append(Token(Atom.EXEC_START))
                    else:
                        tokens.append(Token(Atom.IF_START))

                else:
                    if code[0] == "└":
                        tokens.append(Token(Atom.EXEC_END))
                    else:
                        tokens.append(Token(Atom.IF_END))

                    tokens.append(Token(Atom.BOX_END))

            else:
                singles = {
                    "◇": Atom.MEM,
                    "◈": Atom.ASSIGN,
                    "▔": Atom.NOT,
                    "░": Atom.AND,
                    "▒": Atom.XOR,
                    "▓": Atom.OR,
                    "▚": Atom.L_SHIFT,
                    "▞": Atom.R_SHIFT,
                    "▕": Atom.L_PAREN,
                    "▏": Atom.R_PAREN,
                    "▭": Atom.OUT,
                    "▯": Atom.IN,
                    "\n": Atom.NEWLINE,
                }

                if code[0] in singles:
                    tokens.append(Token(singles[code[0]]))

            code = code[1:]

    return tokens
