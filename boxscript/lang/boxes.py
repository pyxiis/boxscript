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

def neighbors(text, pos):
    r, c = pos
    chars = [[*line] for line in text.splitlines()]
    near = {"N": "\0", "S": "\0", "E": "\0", "W": "\0"}

    try:
        near["E"] = chars[r][c+1]
    except IndexError:
        pass
    
    try:
        near["W"] = chars[r][c-1]
    except IndexError:
        pass

    try:
        near["S"] = chars[r+1][c]
    except IndexError:
        pass

    try:
        near["N"] = chars[r-1][c]
    except IndexError:
        pass

    return near

def valid(text):
    for i, line in enumerate(text.splitlines()):
        # TODO: check extraneous characters

        # check continuity
        for j, char in enumerate(line):
            if "║" in line[:j] and "║" in line[j+1:]:
                continue
            
            expected = ADJACENT.get(char, dict())

            neighbor = neighbors(text, (i, j))

            for direction, expected_neighbors in expected.items():
                if neighbor[direction] not in expected_neighbors:
                    return False, i, j

    return True, -1, -1
