"""Validate an input string.

This module provides the necessary functions to validate boxes in BoxScript code.

Attributes:
    ADJACENT (dict[str, dict[str, str]]): A dictionary of borders and their allowed
        neighbors, organized by relative cardinal location.
    CHARACTERS (str): The set of valid characters in BoxScript code outside of comments.
    BORDERS (str): The set of valid border characters in BoxScript code.

Note:
    The validation here passing does not necessarily mean that the syntax is correct.
    Much of the checking will be done when actually executing the code. Furthermore, the
    interpreter will actually ignore many of the errors (e.g. not enough inputs to a
    binary operation) and will execute the code regardless.
"""

import re
from typing import Optional

__all__ = ["valid"]


ADJACENT = {
    "│": {"N": "│├┤┌┐┞┦┡┩", "S": "│├┤└┘┟┧┢┪"},
    "┃": {"N": "┃┣┫┏┓┟┧┢┪", "S": "┃┣┫┗┛┞┦┡┩"},
    "║": {"N": "║╠╣╔╗", "S": "║╠╣╚╝"},
    "─": {"E": "─┐┘┤┦┧", "W": "─┌└├┞┟"},
    "━": {"E": "━┓┛┫┪┩", "W": "━┏┗┣┢┡"},
    "═": {"E": "═╗╝╣", "W": "═╔╚╠"},
    "┌": {"S": "│├└┟┢", "E": "─┐"},
    "┐": {"S": "│┤┘┧┪", "W": "─┌"},
    "└": {"N": "│├┌┞┡", "E": "─┘"},
    "┘": {"N": "│┤┐┦┩", "W": "─└"},
    "┏": {"S": "┃┣┗┞┡", "E": "━┓"},
    "┓": {"S": "┃┫┛┦┩", "W": "━┏"},
    "┗": {"N": "┃┣┏┟┢", "E": "━┛"},
    "┛": {"N": "┃┫┓┧┪", "W": "━┗"},
    "╔": {"S": "║╠╚", "E": "═╗"},
    "╗": {"S": "║╣╝", "W": "═╔"},
    "╚": {"N": "║╠╔", "E": "═╝"},
    "╝": {"N": "║╣╗", "W": "═╚"},
    "├": {"N": "│├┌┞┡", "S": "│├└┟┢", "E": "─┤"},
    "┤": {"N": "│┤┐┦┩", "S": "│┤┘┧┪", "W": "─├"},
    "┞": {"N": "┃┣┏┟┢", "S": "│├└┟┢", "E": "─┦"},
    "┦": {"N": "┃┫┓┧┪", "S": "│┤┘┧┪", "W": "─┞"},
    "┟": {"N": "│├┌┞┡", "S": "┃┣┗┞┡", "E": "─┧"},
    "┧": {"N": "│┤┐┦┩", "S": "┃┫┛┦┩", "W": "─┟"},
    "┣": {"N": "┃┣┏┟┢", "S": "┃┣┗┞┡", "E": "━┫"},
    "┫": {"N": "┃┫┓┧┪", "S": "┃┫┛┦┩", "W": "━┣"},
    "┡": {"N": "┃┣┏┟┢", "S": "│├└┟┢", "E": "━┩"},
    "┩": {"N": "┃┫┓┧┪", "S": "│┤┘┧┪", "W": "━┡"},
    "┢": {"N": "│├┌┞┡", "S": "┃┣┗┞┡", "E": "━┪"},
    "┪": {"N": "│┤┐┦┩", "S": "┃┫┛┦┩", "W": "━┢"},
    "╠": {"N": "║╠╔", "S": "║╠╚", "E": "═╣"},
    "╣": {"N": "║╣╗", "S": "║╣╝", "W": "═╠"},
}


CHARACTERS = " │┃║─━═┌┐└┘┏┓┗┛╔╗╚╝├┤┞┦┟┧┣┫┡┩┢┪╠╣▄▀◇◈▔░▒▓▚▞▕▏▭▯▖▗▘▝▌▐▧▨▤▥"
BORDERS = "┛┣─├┌│┤┡┏┧┪┟┞━┓┐┢└┦┩┗┫┃┘╔╗╚╝║╠═╣"


def _neighbors(text: str, pos: list[int]) -> dict[str, str]:
    """Finds the characters neighboring a position

    Args:
        text (str): The text to use when finding neighbors
        pos (list[int]): The location in the form [row, column]

    Returns:
        dict[str, str]: A dictionary of neighbors of the form
            {"N": `chr`, "S": `chr`, "E": `chr`, "W": `chr`}.
            If there is no neighboring character in a cardinal direction,
            then that `chr` will be \0.
    """
    r, c = pos
    chars = [[*line] for line in text.splitlines()]
    near = {}

    find = {
        "E": lambda: chars[r][c + 1],
        "W": lambda: chars[r][c - 1],
        "S": lambda: chars[r + 1][c],
        "N": lambda: chars[r - 1][c],
    }

    for direction in find:
        try:
            near[direction] = find[direction]()
        except IndexError:
            near[direction] = "\0"

    return near


def valid(text: str) -> Optional[SyntaxError]:
    """Checks whether the code only contains valid boxes

    Args:
        text (str): The code to check

    Returns:
        Optional[SyntaxError]: The syntax error, if any.
    """
    lines = text.splitlines()

    # check continuity
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if "║" in line[:j] and "║" in line[-~j:]:
                continue

            expected = ADJACENT.get(char, {})

            neighbor = _neighbors(text, (i, j))

            for direction, expected_neighbors in expected.items():
                if neighbor[direction] not in expected_neighbors:
                    return SyntaxError(f"Discontinuous box at line {i}")

    for i, line in enumerate(lines):
        # remove comments
        strip_c = line
        for comment in re.findall(r"║.*║", line):
            strip_c = strip_c.replace(comment, " " * len(comment))

        # check for invalid characters
        for _j, char in enumerate(strip_c):
            if char not in CHARACTERS:
                return SyntaxError(f"Invalid character `{char}` at line {i}")

        # check for duplicate boxes
        if len(re.findall(r"[┌┐└┘┏┓┗┛╔╗╚╝]", strip_c)) not in (0, 2):
            return SyntaxError(f"Duplicate box at line {i}")

        # remove whitespace
        strip_w = re.sub(r"\s", "", strip_c)

        # check for duplicate/malformed boxes
        if re.match(r".*[┌┐┏┓╔╗]", strip_w):
            sides = re.split(r"[┌┏╔].*[┐┓╗]", strip_w)

            if len(re.findall(r"[│┃]", sides[0])) != len(re.findall(r"[│┃]", sides[1])):
                return SyntaxError(f"Duplicate box at line {i}")

        # check for unmatched walls
        sides = [walls for walls in re.split(r"[^│┃║]+", strip_w)] if strip_w else []

        if sides:
            if len(sides) != 2:
                if sides[0] != sides[0][::-1]:
                    return SyntaxError(f"Unmatched wall at line {i}")

            elif sides[0] != sides[1][::-1]:
                return SyntaxError(f"Unmatched wall at line {i}")

        # check that no code is outside of a box
        strip_w = re.sub(r"[╔╚║╠].*[╗╝║╣]", "", strip_w)

        statements = re.findall(fr"[^{BORDERS}]+", strip_w)
        borders = re.findall(fr"[{BORDERS}]", strip_w)

        if strip_w and not borders:
            print(strip_w)
            return SyntaxError(f"Code outside of box at line {i}")

        if any(char in strip_w for char in "┛┣─├┌┤┡┏┧┪┟┞━┓┐┢└┦┩┗┫┘"):
            if len(statements) > 0:
                return SyntaxError(f"Code outside of box at line {i}")
        else:
            if len(statements) > 1:
                return SyntaxError(f"Code outside of box at line {i}")
