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

Numbers are the only form of data in BS. The first digit is always the sign of the number, with `▀` being positive and `▄` being negative. The postceding digits are the actual number in binary, with 0 being `▄` and 1 being `▀`. `▣` is a delimiter which functions like a decimal point in human-readable numbers. `▀▄▣▄▀` would therefore represent 0.25.

### Memory

`◇` represents an array which can store an arbitrary number of numbers.
Each cell can be accessed by its index, where the index is a number immediately postceding the `◇`. Hence, `◇▀▄` would represent the 0th cell.

Interestingly, unlike an array, any number can be used as an index. Cells have 0 as their default value. Since the actual implementation uses a hashmap-like object, even noninteger indices can be used.

## Operators

Unary operators are invoked in this form: `<operator> A`.

Binary operators are invoked in this form: `A <operator> B`.

Spaces are not necessary between terms.

### Comparison

These operators are all binary.

`▨` is equivalent to `<` in most languages.
Similarly, `▧` is equivalent to `>` and `▤` is equivalent to `==`.
`▨▤` and `▧▤` are equivalent to `<=` and `>=`, respectively.
Lastly, `▥` is equivalent to `!=`.

In order to maintain the fact that BS only has numbers, booleans are represented by 0 or 1.

### Bitwise

`▔` represents NOT. This is a unary operator.

The following bitwise operators are all binary.

`░` represents AND. `▒` represents XOR. `▓` represents OR. `▚` represents left shift. `▞` represents right shift.

### Arithmetic

These operators are all binary.

`▦` is the addition operator. The multiplication operator is `▩`. There are no other arithmetic operators. Subtraction and division are done through adding/multiplying additive/multiplicative inverses.

### Order of Operations

The order of operations, from lowest to highest precedence, is:

- Output/assignment
- Comparison operators (e.g. `▨`, `▧`, `▤`)
- OR (`▓`)
- XOR (`▒`)
- AND (`░`)
- Shifts (`▚`, `▞`)
- Addition (`▦`)
- Multiplication (`▩`)
- NOT (`▔`)

Should this order be undesireable, expressions put between `▕` and `▏` will be evaluated first. These are essentially opened and closed parentheses, respectively. For example, `▔▕▀▀▀▨▀▀▄▏▩▀▀▄▀` should evaluate to `▄▀▄▀`.

## IO

`▭` outputs the postceding value. `▯` represents input, and can be accessed similarly to `◇`.
