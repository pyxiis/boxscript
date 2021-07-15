from enum import Enum
import functools
import re
from typing import Any

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


class Token:
    """A BoxScript Token

    Attributes:
        attr1 (Atom): The type of token
        attr2 (Any, optional): The value of the token—only exists for NUM tokens
    """

    def __init__(self, type: Atom, value: Any = None):
        """Creates a BoxScript token.

        Args:
            type (Atom): The type of token
            value (Any, optional):  The value of the token—only exists for NUM tokens.
                Defaults to None.
        """
        self.type = type
        self.value = value

    def __str__(self) -> str:
        """Returns a string representation of the token

        Returns:
            str: The token's string representation
        """
        if self.value:
            return f"{self.type.name}: {self.value}"
        return f"{self.type.name}"


def tokenize(code: str) -> list[Token]:
    """Creates a list of tokens from BS code

    Args:
        code (str): The input code

    Returns:
        list[Token]: The list of BS tokens
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
