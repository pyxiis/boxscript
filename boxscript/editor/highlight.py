from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.theme import Theme


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
    )

    BoxScriptHighlighter().highlight(t)

    Console(theme=theme).print(
        Panel(t, highlight=True, title="test.bs", style=Style(bgcolor="#36393f"))
    )
