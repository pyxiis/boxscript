ADJACENT = {
    "│": {"N": "│├┤┌┐┞┦┡┩", "S": "│├┤└┘┟┧┢┪"},
    "┃": {"N": "┃┣┫┏┓┟┧┢┪", "S": "┃┣┫┗┛┞┦┡┩"},
    "║": {"N": "║╠╣╔╗", "S": "║╠╣╚╝"},
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


def neighbors(text: str, pos: list[int]) -> dict[str, str]:
    """Finds the characters neighboring a position

    Args:
        text (str): The text to use when finding neighbors
        pos (list[int]): The location in the form [row, column]

    Returns:
        dict[str, str]: A dictionary of neighbors of the form {"N": `chr`, "S": `chr`, "E": `chr`, "W": `chr`}.
            If there is no neighboring character in a cardinal direction, then that `chr` will be \0.
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


def valid(text: str) -> tuple[bool, int, int]:
    """Checks whether the code only contains valid boxes

    Args:
        text (str): The text to check

    Returns:
        tuple[bool, int, int]: Whether the text is valid, and where the first found error is if it exists
    """
    for i, line in enumerate(text.splitlines()):
        # TODO: check extraneous characters

        # check continuity
        for j, char in enumerate(line):
            if "║" in line[:j] and "║" in line[-~j:]:
                continue

            expected = ADJACENT.get(char, dict())

            neighbor = neighbors(text, (i, j))

            for direction, expected_neighbors in expected.items():
                if neighbor[direction] not in expected_neighbors:
                    return False, i, j

    return True, -1, -1
