# Examples

## Printing 0-9

```bs
╔═══════════════════╗
║ output 0123456789 ║
╚═══════════════════╝

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
```

At first glance, this may seem very hard to read. And that's because it is!
BS is an esoteric language, like Brainfuck or Hexagony. It is not meant to be practical! But nonetheless, let us break this code down.

The first 3 lines are comments. These are ignored by the interpreter, unless they present a syntax error.

As it would be tedious to explain how everything works, here is the line-by-line Python translation:

```py
"""
Output 0123456789
"""

while True:
    if not m[+0] ^ +10: break

    m[+1] = m[+0] ^ +48
    m[+2] = m[0] & +48

    while True:
        if not m[+2]: break

        m[+3] = m[+2] << +1
        m[+2] = m[+1] & m[+3]
        m[+1] = m[+1] ^ m[+3]

    print(chr(m[+1]))

    m[+1] = m[+0] & +1
    m[+0] = m[+0] ^ +1

    while True:
        if not m[+1]: break

        m[+2] = m[+1] << +1
        m[+1] = m[+0] & m[+2]
        m[+0] = m[+0] ^ m[+2]
```

## Hello World

We can also write a program which outputs "Hello, world!".

The code below will not be explained, but exists because every language needs a "Hello, world!" program.

```bs
╔══════════════════════╗
║ output Hello, world! ║
╚══════════════════════╝

┌─────────┐
│▭▀▀▄▄▀▄▄▄│
│▭▀▀▀▄▄▀▄▀│
│▭▀▀▀▄▀▀▄▄│
│▭▀▀▀▄▀▀▄▄│
│▭▀▀▀▄▀▀▀▀│
│▭▀▀▄▀▀▄▄ │
│▭▀▀▄▄▄▄▄ │
│▭▀▀▀▀▄▀▀▀│
│▭▀▀▀▄▀▀▀▀│
│▭▀▀▀▀▄▄▀▄│
│▭▀▀▀▄▀▀▄▄│
│▭▀▀▀▄▄▀▄▄│
│▭▀▀▄▄▄▄▀ │
└─────────┘
```
