import numpy

from boxscript.box import matrix


def test_matrix():
    """Test for matrix"""
    numpy.testing.assert_array_equal(
        matrix("hello\nworld"),
        numpy.array([["h", "e", "l", "l", "o"], ["w", "o", "r", "l", "d"]]),
    )

    numpy.testing.assert_array_equal(
        matrix("hello\nhi"),
        numpy.array([["h", "e", "l", "l", "o"], ["h", "i", "\0", "\0", "\0"]]),
    )

    numpy.testing.assert_array_equal(
        matrix("a\nbc\ndef"),
        numpy.array([["a", "\0", "\0"], ["b", "c", "\0"], ["d", "e", "f"]]),
    )
