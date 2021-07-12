from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.syntax import Syntax
from rich.theme import Theme


class BoxScriptHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "token."
    highlights = [
        r"(?P<border>[─━│┃┌┍┎┏┐┑┒┓└┗┘┛├┞┟┡┢┣┤┦┧┩┪┫])",
        r"(?P<op>[▨▧▤▥▔░▒▓▚▞▦▩◈])",
        r"(?P<number>[▄▀▣]*)",
        r"(?P<memory>◇[▄▀▣]*)",
        r"(?P<io>[▭▯])",
        r"(?P<paren>[▕▏])",
        r"(?P<comment>.*[═║].*)",
    ]


theme = Theme(
    {
        "token.border": "bright_black",
        "token.op": "bright_red",
        "token.number": "bright_magenta",
        "token.memory": "bright_green",
        "token.io": "bright_cyan",
        "token.paren": "bright_white",
        "token.comment": "bright_black",
    }
)

console = Console(highlighter=BoxScriptHighlighter(), theme=theme)
console.print(
    Panel(Syntax(
        """
╔═══════════════════╗
║ output 0123456789 ║
╚═══════════════════╝

┏━━━━━━━━━━━━┓
┃◇▀▄▨▀▀▄▀▄   ┃
┡━━━━━━━━━━━━┩
│▭◇▀▄▦▀▀▀▄▄▄▄│
├────────────┤
│◇▀▄◈▕◇▀▄▦▀▀▏│
└────────────┘
""", "python", line_numbers=True),
        title="test.bs"
    )
)
