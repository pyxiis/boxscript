import io
import unittest
from contextlib import redirect_stdout
from textwrap import dedent

from boxscript.interpreter import Interpreter


def run_code(code: str) -> str:
    """Test helper method to run provided boxscript."""
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        Interpreter().run(code)
    return stdout.getvalue()


class TestExecution(unittest.TestCase):
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
        s = dedent(s).strip()
        self.assertEqual(run_code(s), "0\n")

    def test_01234567_bitwise(self) -> None:
        """Output: 01234567"""
        s = """
            ╔═══════════════════╗
            ║ output 0123456789 ║
            ╚═══════════════════╝

            ┏━━━━━━━━━━━━━━━━┓
            ┃◇▀▄▒▀▀▄▀▄       ┃
            ┡━━━━━━━━━━━━━━━━┩
            │▀▀◈◇▀▄▒▀▀▀▄▄▄▄  │
            │▀▀▄◈◇▀▄░▀▀▀▄▄▄▄ │
            │┏━━━━━━━━━━━━━┓ │
            │┃◇▀▀▄         ┃ │
            │┡━━━━━━━━━━━━━┩ │
            ││▀▀▀◈◇▀▀▄▚▀▀  │ │
            ││▀▀▄◈◇▀▀░◇▀▀▀ │ │
            ││▀▀◈◇▀▀▒◇▀▀▀  │ │
            │└─────────────┘ │
            │▭◇▀▀            │
            ├────────────────┤
            │▀▀◈◇▀▄░▀▀       │
            │▀▄◈◇▀▄▒▀▀       │
            │┏━━━━━━━━━━━━┓  │
            │┃◇▀▀         ┃  │
            │┡━━━━━━━━━━━━┩  │
            ││▀▀▄◈◇▀▀▚▀▀  │  │
            ││▀▀◈◇▀▄░◇▀▀▄ │  │
            ││▀▄◈◇▀▄▒◇▀▀▄ │  │
            │└────────────┘  │
            └────────────────┘
            """
        s = dedent(s).strip()
        self.assertEqual(run_code(s), "0123456789\n")

    def test_01234567(self) -> None:
        """Output: 0123456789"""
        s = """
            ┏━━━━━━━━━━━━┓
            ┃◇▀▄▨▀▀▄▀▄   ┃
            ┡━━━━━━━━━━━━┩
            │▭◇▀▄▐▀▀▀▄▄▄▄│
            ├────────────┤
            │▀▄◈◇▀▄▐▀▀   │
            └────────────┘
            """
        s = dedent(s)
        self.assertEqual(run_code(s), "0123456789\n")

    def test_invalid_code(self) -> None:
        """Provide invalid code"""
        s = """
            ╔═══════════════════════╗
            ║This code does nothing ║
            ╚═══════════════════════╝
            ┏━━━━━━━━━━━━━━━━┓
            ┃◇▀▄▒▀▀▄▀▄       ┃
            ┡━━━━━━━━━━━━━━━━┩
            │◇▀▀◈◇▀▄▒▀▀▀▄▄▄▄ │
            │◇▀▀▄◈◇▀▄░▀▀▀▄▄▄▄│
            │┏━━━━━━━━━━━━━┓ │
            │┃◇▀▀▄         ┃ │
            │┡━━━━━━━━━━━━━┩ │
            ││◇▀▀▀◈◇▀▀▄▚▀▀ │ │
            ││◇▀▀▄◈◇▀▀░◇▀▀▀│ │
            ││◇▀▀◈◇▀▀▒◇▀▀▀ │ │
            │└─────────────┘ │
            │╔═════════════╗ │
            │║Test [orange]║ │
            │╚═════════════╝ │
            │▭◇▀▀            │
            ├────────────────┤
            │◇▀▀◈◇▀▄░▀▀      │
            │◇▀▄◈◇▀▄▒▀▀      │
            │┏━━━━━━━━━━━━┓  │
            │┃◇▀▀         ┃  │
            │┡━━━━━━━━━━━━┩  │
            ││◇▀▀▄◈◇▀▀▚▀▀ │  │
            ││◇▀▀◈◇▀▄░◇▀▀▄│  │
            ││◇▀▄◈◇▀▄▒◇▀▀▄│  │
            │└────────────┘  │
            └────────────────┘
            """
        s = dedent(s).strip()
        self.assertRaises(Exception, run_code(s))
