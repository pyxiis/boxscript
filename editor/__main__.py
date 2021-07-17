import math

from blessed import Terminal
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.theme import Theme

co = Console()


class BoxScriptHighlighter(RegexHighlighter):
    """Highlighter for BS syntax"""

    base_style = "token."
    highlights = [
        r"(?P<border>[─━│┃┌┍┎┏┐┑┒┓└┗┘┛├┞┟┡┢┣┤┦┧┩┪┫])",
        r"(?P<op>[▨▧▤▥▔░▒▓▚▞▦▩◈])",
        r"(?P<number>[▄▀▣]*)",
        r"(?P<memory>◇[▄▀▣]*)",
        r"(?P<io>[▭▯])",
        r"(?P<paren>[▕▏])",
        r"(?P<comment>║[^\n]*║|[╔╚]═*[╗╝])",
    ]


if __name__ == "__main__":
    # please customize this!
    theme = Theme(
        {
            "token.border": "#ffffff",
            "token.op": "#edb9b6",
            "token.number": "#d5b6ed",
            "token.memory": "#b6edb9",
            "token.io": "#b6eaed",
            "token.paren": "#b9b6ed",
            "token.comment": "#18191c",
        }
    )
    t = Text(
        """
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
        """
    )

    BoxScriptHighlighter().highlight(t)

    Console(theme=theme).print(
        Panel(t,
            highlight=True,
            title="test.bs",
            width=50,
            height=75,
            style=Style(bgcolor="#36393f")
        )
    )
"""
    )

term = Terminal()

dictofletters = {
    "r": "▀",
    "w": "◇",
    "e": "◈",
    "t": "▄",
    "y": "▒",
    "u": "░",
    "i": "▭",
    "o": "▒",
}


def main() -> None:
    """Main function."""
    row_length = 10
    max_row_length = math.floor(term.width / 2)
    print(f"{term.home}{term.white_on_black}{term.clear}")
    print("press 'q' to quit.")
    with term.cbreak():  # While you are pressing buttons
        val = ""
        ll = ""
        # max_row_length = len(val)
        while ll.lower() != "q":  # While the button is not q
            ll = term.inkey()

            if val.count("\n") == 0:
                max_row_length = len(val)

            if ll.name == "KEY_BACKSPACE":  # Delete Char
                val = val[:-1]

            elif ll.name == "KEY_ENTER":  # New line
                val += "\n"
                if row_length > max_row_length:
                    max_row_length = row_length
                    row_length = 0

            else:
                val += dictofletters.get(ll, ll)  # Write Char
                row_length += 1

            print(f"{term.clear}")

            Console(theme=theme).print(
                Panel(
                    val,
                    highlight=True,
                    title="test.bs",
                    width=max_row_length,
                    style=Style(bgcolor="#36393f"),
                )
            )

        print(f"send help!{term.normal}")


main()
