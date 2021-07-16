from pygments.lexer import RegexLexer
from pygments.token import Literal, Token


class BSLexer(RegexLexer):
    """A Pygments lexer for BoxScript."""

    name = 'BS'
    aliases = ['box', 'bs', 'boxscript']
    filenames = ['*.bs']

    tokens = {
        'root': [
            (r'[─━│┃┌┍┎┏┐┑┒┓└┗┘┛├┞┟┡┢┣┤┦┧┩┪┫]', Token.Text),
            (r'[▔░▒▓▚▞◈]', Token.Operator),
            (r'◇[▄▀]*|[▄▀]+(?=◈)', Literal.String),
            (r'[▄▀]+', Literal.Number),
            (r'[▭▯]', Token.Keyword),
            (r'[▕▏]', Token.Punctuation),
            (r'║[^\n]*║|[╔╚]═*[╗╝]', Token.Comment),
            (r'\s', Token.Text.Whitespace),
            (r'.', Token.Generic)
        ]
    }

# pygments.highlight(t, BSLexer(), Terminal256Formatter(linenos=True))
