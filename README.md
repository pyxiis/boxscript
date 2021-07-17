# BoxScript

![logo](./logo.png)

BoxScript, or BS for short, is a language based on the idea of "boxes".

What are boxes, exactly? Boxes, and their younger sibling, blocks, are simply units of code. They can be loops, conditionals, or anything else, really. Expressions with different purposes go into different blocks, and blocks with different functions go into different boxes. Sounds simple, right?

BoxScript's most defining feature is encouraging **thinking inside the box** when writing code—literally, since no code can exist outside of a box. If that's not BS, then what is?

## Installation

1. Clone the repository

```sh
git clone https://github.com/somthecoder/CodeJam-Discrete-Dingos.git
```

2. Install the dependencies

```sh
pip install -r requirements.txt
```

## Requirements

* Python 3.9+
* A font which supports [Block Elements](https://www.unicode.org/charts/PDF/U1FB00.pdf), [Box Drawing](https://www.unicode.org/charts/PDF/U2500.pdf), and [Geometric Shapes](https://unicode.org/charts/PDF/U25A0.pdf)

## Running

You can try running the editor through this command:

```sh
python -m editor
```

Admittedly, the editor is pretty low quality, but you can actually execute BoxScript code directly from a file!

Put this file in the root directory, and run it—be sure to replace the file path with the path to your file.

```py
from boxscript.interpreter import Interpreter

with open('docs/helloworld.bs') as bs:
    Interpreter().run(bs.read())
```

## Contributors

* [エニラ#0013](https://github.com/pyxiis): Programmer
* [A Real Username#8028](https://github.com/onerandomusername): Debugger
* [Slipperee_Slime#3232](https://github.com/Slipperee-CODE): Slime
* [No u#6720](https://github.com/somthecoder): Leader
