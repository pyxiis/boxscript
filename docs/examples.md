# Examples

## Printing 0-9

```bs
╔═══════════════════╗
║ output 0123456789 ║
╚═══════════════════╝

┏━━━━━━━━━━━━┓
┃◇▀▄▨▀▀▄▀▄   ┃
┡━━━━━━━━━━━━┩
│▭◇▀▄▦▀▀▀▄▄▄▄│
├────────────┤
│◇▀▄◈◇▀▄▦▀▀  │
└────────────┘
```

At first glance, this may seem very hard to read. And that's because it is!
BS is an esoteric language, like Brainfuck or Hexagony. It is not meant to be practical! But nonetheless, let us break this code down.

The first 3 lines are comments. These are ignored by the interpreter, unless they present a syntax error.

Lines 5-7 have a bolded border. Notice how it is ambiguous what the bottom border of this box should be—is it bold because of the code above or normal because of the code below? This does not matter. Do as you please.

Anyways, back to lines 5-7. The code which is checked is `◇▀▄▨▀▀▄▀▄`.
There are a few parts to this code:

- `◇` represents memory.
  - You can access a memory cell by writing `◇` followed by a number, as seen in `◇▀▄`. These cells default to 0, but support any real number. Numbers will be covered later.
- `▨` is equivalent to `<` in most languages. Similarly, `▧` is equivalent to `>` and `▤` is equivalent to `==`.
- `▀▀▄▀▄` is a number—10. Numbers are the only data type BS supports.
The first digit is always the sign of the number, with `▀` being positive and `▄` being negative. The postceding digits are the actual number in binary, with 0 being `▄` and 1 being `▀`. `▣` is a delimiter which functions like a decimal point in human-readable numbers. `▀▄▣▄▀` would therefore represent 0.25.

The conditional checks whether the 0th cell in memory is less than 10.

Lines 7-11 are executed code. The border between lines 8 and 10 is not mandatory, but it is recommended by BS's BDFL.

`▭◇▀▄▦▀▀▀▄▄▄▄` is interpreted like this:

- `▭` is the output function. It outputs the Unicode character corresponding to the number given.
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

## Hello World

Using the knowledge from the previous example, we can now write a program which outputs "Hello, world!".

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
