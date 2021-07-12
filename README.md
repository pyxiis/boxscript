# BoxScript

## Syntax

BoxScript, or BS for short, is a language based on the idea of "boxes".

### Boxes

A box is simply a bordered container of code.
Here are some examples of empty boxes:

```bs
┌────────────┐
│            │
└────────────┘
```

```bs
┏━━━━┓
┃    ┃
┡━━━━┩
│    │
└────┘
```

```bs
╔═══════════════════╗
║                   ║
╚═══════════════════╝
```

Note that box must have continuous edges (that is, edges which conform to their surrouning edges).

A box is defined by having 4 corners. In the first box, `┌`, `┐`, `└`, and `┘` are corners. In the second box, `┏`, `┓`, `└`, and `┘` are corners. In the third box, `╔`, `╗`, `╚`, and `╝` are corners.

Boxes can be nested (if we have time), and are executed from top to bottom.
No more than 1 box of the same level may occupy the same row.

### Blocks

Notice how in the second example, there are 3-junctions: `┡` and `┩`.
These denote the separation of chunks of code.
Any transition between border styles must be done by a 3-junction or by initiating another box.
This means that characters such as `╽` and `╿` are not allowed.

Each border type has a specific meaning.

Normal borders are simply executed code.

Bolded borders represent conditionals. In BS, each box actually represents a loop. If there are no conditionals, the loop is executed once. Otherwise, the loop will execute until at least one conditional is false.

Doubled borders are comments.
Why? Because they don't share appropriate 3-junction characters with the other border styles. This means that they cannot connect with meaningful code, and therefore, are difficult to find a use-case for.

### Example

We are now ready to start writing some code. Take a look at the following example:

```bs
╔═══════════════════╗
║ output 0123456789 ║
╚═══════════════════╝

┏━━━━━━━━━━━━┓
┃◇▀▄▨▀▀▄▀▄   ┃
┡━━━━━━━━━━━━┩
│◇▀▄◈◇▀▄▦▀▀  │
├────────────┤
│□◇▀▄▦▀▀▀▄▄▄▄│
└────────────┘
```

At first glance, this may seem very hard to read. And that's because it is!
BS is an esoteric language, like Brainfuck or Hexagony. It is not meant to be practical! But nonetheless, let us break this code down.
