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

Note that box must have continuous edges (that is, edges must conform to their surrounding edges).

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

## Examples

We are now ready to start writing some code.
Explanations will sometimes be provided.

### Printing 0-9

```bs
╔═══════════════════╗
║ output 0123456789 ║
╚═══════════════════╝

┏━━━━━━━━━━━━┓
┃◇▀▄▨▀▀▄▀▄   ┃
┡━━━━━━━━━━━━┩
│□◇▀▄▦▀▀▀▄▄▄▄│
├────────────┤
│◇▀▄◈◇▀▄▦▀▀  │
└────────────┘
```

At first glance, this may seem very hard to read. And that's because it is!
BS is an esoteric language, like Brainfuck or Hexagony. It is not meant to be practical! But nonetheless, let us break this code down.

The first 3 lines are comments. These are ignored by the interpreter, unless they present a syntax error.

Lines 5-7 have a bolded border. Notice how it is ambiguous what the bottom border of this box shoul be—is it bold because of the code above or normal because of the code below? This does not matter. Do as you please.

Anyways, back to lines 5-7. The code which is checked is `◇▀▄▨▀▀▄▀▄`.
There are a few parts to this code:

- `◇` represents memory.
  - You can access a memory cell by writing `◇` followed by a number, as seen in `◇▀▄`. These cells default to 0, but support any real number. Numbers will be covered later.
- `▨` is equivalent to `<` in most languages. Similarly, `▧` is equivalent to `>` and `▤` is equivalent to `==`.
- `▀▀▄▀▄` is a number—10. Numbers are the only data type BS supports.
The first digit is always the sign of the number, with `▀` being positive and `▄` being negative. The postceding digits are the actual number in binary, with 0 being `▄` and 1 being `▀`. `▥` is a delimiter which functions like a decimal point in human-readable numbers. `▀▄▥▄▀` would therefore represent 0.25.

The conditional checks whether the 0th cell in memory is less than 10.

Lines 7-11 are executed code. The border between lines 8 and 10 is not mandatory, but it is recommended by BS's BDFL.

`□◇▀▄▦▀▀▀▄▄▄▄` is interpreted like this:

- `□` is the output function. It outputs the Unicode character corresponding to the number given.
- `◇▀▄` is something you should definitely remember from before—the 0th cell of memory.
- `▦` is addition.
- `▀▀▀▄▄▄▄` is 48. We add this because the ASCII code for `0` is 48.

Converting numbers other than the ones shown here to readable output is left as an exercise for the reader.

`◇▀▄◈◇▀▄▦▀▀` when broken down is as follows:

- `◇▀▄` is the 0th cell of memory.
- `◈` is the assignment operator. This is because `◈` "fills in" `◇`. It fills the preceding cell with the postceding value.
- `◇▀▄` was covered before.
- `▦` is the addition operator. The multiplication operator is `▩`. There are no other arithmetic operators, though there do exist bitwise operators. Subtraction and division are done through adding negatives and multiplying by numbers between 0 and 1.
- `▀▀` is 1.

In each iteration, the content of the 0th cell of memory is printed in decimal. The 0th cell then gets incremented by 1.

This code outputs `0123456789`.

### Hello, world!

Using the knowledge from the previous example, we can now write a program which outputs "Hello, world!".

The code below will not be explained, but exists because every language needs a "Hello, world!" program.

```bs
╔══════════════════════╗
║ output Hello, world! ║
╚══════════════════════╝

┌─────────┐
│□▀▀▄▄▀▄▄▄│
│□▀▀▀▄▄▀▄▀│
│□▀▀▀▄▀▀▄▄│
│□▀▀▀▄▀▀▄▄│
│□▀▀▀▄▀▀▀▀│
│□▀▀▄▀▀▄▄ │
│□▀▀▄▄▄▄▄ │
│□▀▀▀▀▄▀▀▀│
│□▀▀▀▄▀▀▀▀│
│□▀▀▀▀▄▄▀▄│
│□▀▀▀▄▀▀▄▄│
│□▀▀▀▄▄▀▄▄│
│□▀▀▄▄▄▄▀ │
└─────────┘
```
