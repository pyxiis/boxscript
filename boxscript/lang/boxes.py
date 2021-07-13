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


CHARACTERS = " │┃║─━═┌┐└┘┏┓┗┛╔╗╚╝├┤┞┦┟┧┣┫┡┩┢┪╠╣▄▀◇◈▔░▒▓▚▞▕▏▭▯"


def neighbors(text: str, pos: list[int]) -> dict[str, str]:
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
    near = {"N": "\0", "S": "\0", "E": "\0", "W": "\0"}

    try:
        near["E"] = chars[r][c + 1]
    except IndexError:
        pass

    try:
        near["W"] = chars[r][c - 1]
    except IndexError:
        pass

    try:
        near["S"] = chars[r + 1][c]
    except IndexError:
        pass

    try:
        near["N"] = chars[r - 1][c]
    except IndexError:
        pass

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

            expected = ADJACENT.get(char, dict())

            neighbor = neighbors(text, (i, j))

            for direction, expected_neighbors in expected.items():
                if neighbor[direction] not in expected_neighbors:
                    return SyntaxError(f"Discontinuous box at line {i}")

    for i, line in enumerate(lines):
        # remove comments
        strip_c = re.sub(r"║.*║", "", line)

        # check for invalid characters
        for j, char in enumerate(strip_c):
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

            if len(re.findall(r"[│┃║]", sides[0])) != len(
                re.findall(r"[│┃║]", sides[1])
            ):
                return SyntaxError(f"Duplicate box at line {i}")

        # check for unmatched walls
        sides = [walls for walls in re.split(r"[^│┃║]+", strip_w) if walls]

        if sides:
            if len(sides) == 1:
                if sides[0] != sides[0][::-1]:
                    return SyntaxError(f"Unmatched wall at line {i}")
            elif sides[0] != sides[1][::-1]:
                return SyntaxError(f"Unmatched wall at line {i}")
