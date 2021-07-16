from contextlib import redirect_stdout
import io
import unittest

from boxscript.ast import Script
from boxscript.lex import tokenize


class TestParsing(unittest.TestCase):
    """Tests boxscript.ast for parsing numbers properly."""

    def test_48_is_zero(self) -> None:
        """48 is 0 in ascii"""
        s = """
╔═════════════════╗
║ 0               ║
╚═════════════════╝

┌───────────────┐
│▭▀▀▀▄▄▄▄       │
└───────────────┘
"""
        t = tokenize(s)
        o = Script(t)
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            o.execute()
        self.assertEqual(stdout.getvalue().strip(), "0")
