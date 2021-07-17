# Syntax

## Boxes

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

Note that boxes must have continuous edges (that is, edges must conform to their surroundings).

A box is defined by having 4 corners. In the first box, `┌`, `┐`, `└`, and `┘` are corners. In the second box, `┏`, `┓`, `└`, and `┘` are corners. In the third box, `╔`, `╗`, `╚`, and `╝` are corners.

Boxes can be nested (if we have time), and are executed from top to bottom.
No more than 1 box of the same level may occupy the same row.

## Blocks

Notice how in the second example, there are 3-junctions: `┡` and `┩`.
These denote the separation of chunks of code.
Any transition between border styles must be done by a 3-junction or by initiating another box.
This means that characters such as `╽` and `╿` are not allowed.

Just as with boxes, no more than 1 block of the same level may occupy the same row.

Each border type has a specific meaning.

Normal borders are simply executed code.

Bolded borders represent conditionals. In BS, each box actually represents a loop. If there are no conditionals, the loop is executed once. Otherwise, the loop will execute until at least one conditional is false.

Doubled borders are comments.
Why? Because they don't share appropriate 3-junction characters with the other border styles. This means that they cannot connect with meaningful code, and therefore, are difficult to find a use-case for.

## Data

### Numbers

Numbers are the only form of data in BS. The first digit is always the sign of the number, with `▀` being positive and `▄` being negative. The postceding digits are the actual number in binary, with 0 being `▄` and 1 being `▀`. `▄▀▄▄▀▄` would therefore represent -18.

### Memory

`◇` represents an array which can store an arbitrary number of numbers.
Each cell can be accessed by its index, where the index is a number immediately postceding the `◇`. Hence, `◇▀▄` would represent the 0th cell.
Each cell has a default value of `▀▄`.

## Operators

Unary operators are invoked in this form: `<operator> A`.

Binary operators are invoked in this form: `A <operator> B`.

Left associative operators are evaluated from left to right.

Right associative operators are evaluated from right to left.

Spaces are not necessary between terms.

### Comparison

All comparison operators are binary and left-associative.

- `▨` represents less than.
- `▧` represents greater than.
- `▤` represents equal to.
- `▥` represents not equal to.

These operators return `▀▄` if false, and otherwise return `▀▀`.

### Assignment

`◈` is the assignment operator. This is because `◈` "fills in" `◇`. It fills the preceding cell with the postceding value. Note that the preceding cell should be a memory index.

There may only be one assignment operation per line.

### Bitwise

`▔` represents NOT. This is a unary operator.

The following bitwise operators are all binary and left-associative.

- `░` represents AND.
- `▒` represents XOR.
- `▓` represents OR.
- `▚` represents left shift.
- `▞` represents right shift.

### Arithmetic

All arithmetic operators are binary. The exponentiation operator is right-associative, but all other arithmetic operators are left-associative.

- `▐` represents addition.
- `▌` represents subtraction.
- `▘` represents multiplication.
- `▝` represents division.
- `▗` represents modulo.
- `▖` represents exponentiation.

Do note that while floats cannot be stored, they are used when processing intermediate steps.

### Order of Operations

The order of operations, from lowest to highest precedence, is:

- Output/assignment
- Less than, greater than, equal to, not equal to (`▨`, `▧`, `▤`, `▥`)
- OR (`▓`)
- XOR (`▒`)
- AND (`░`)
- Left shift, right shift (`▚`, `▞`)
- Addition, subtraction (`▐`, `▌`)
- Multiplication, division, modulo (`▘`, `▝`, `▗`)
- Memory access
- NOT (`▔`)
- Exponentiation (`▖`)

When there are 2 operations of the same precedence, they are done from left to right.

Should this order be undesireable, expressions put between `▕` and `▏` will be evaluated first. These are essentially opened and closed parentheses, respectively. For example, `▀▀▒▔▕▀▀▀░▀▀▄▏` should evaluate to `▄▀▄▄`.

## IO

`▭` outputs the postceding value. There may only be one output operation per line.
