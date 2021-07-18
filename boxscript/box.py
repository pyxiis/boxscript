import numpy


def matrix(code: str) -> numpy.ndarray:
    """Converts a string into a matrix.

    Args:
        code (str): The input string to convert to a matrix

    Returns:
        numpy.ndarray: The 2D matrix of the string's chars.
    """
    lines = code.splitlines()
    length = max(map(len, lines))
    return numpy.array([[*line.ljust(length, "\0")] for line in lines], dtype="str")
