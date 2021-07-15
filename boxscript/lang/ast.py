from lang.lex import Atom, Node, Token


class Container(Node):
    """A node which contains semi-parsed code, such as other Containers, as children."""

    __slots__ = ["children"]

    def __init__(self, children: list[Node] = None):
        """Create a new container.

        Args:
            children (list, optional): The children of the Container. Defaults to None.
        """
        self.children = children or []

    def execute(self) -> int:
        """Executes all children.

        Returns:
            int: The outcome of the last execution.
        """
        r = 0
        for child in self.children:
            r = child.execute()
        return r


class Block(Container):
    """A class representing a "block" of code."""


class IfBlock(Block):
    """A class for denoting conditional blocks of code."""


class ExecBlock(Block):
    """A class for denoting executable blocks of code."""


class Box(Container):
    """A class for denoting a single "box" of code.

    This is a loop in other languages. Sort of.
    """

    def execute(self) -> int:
        """Executes all children.

        Returns:
            int: 0 if a conditional fails, 1 otherwise. Infinite loops will give an
                error because Python does not support infinite loops. Essentially,
                any box which has a conditional will return 0.
        """
        conditional = any(isinstance(child, IfBlock) for child in self.children)
        if conditional:
            for child in self.children:
                value = child.execute()
                if isinstance(child, IfBlock) and not value:
                    return 0
            self.execute()
        else:
            for child in self.children:
                child.execute()
        return 1


class Line(Container):
    """A class for a line of code.

    Note:
        A line cannot contain any other Containers. A line is the most primitive
        "chunk" of code.

    Todo:
        * Actually parse out a line of code into a tree.
    """

    def execute(self) -> int:
        """Executes all children

        Returns:
            int: The outcome of the execution.
        """

        # tree code here

        if self.children:
            return self.children[0].execute()
        else:
            return 0


class Script(Container):
    """A class for the Container which contains all code.

    This class is needed because the script must be parsed into Containers, which is
        done in the __init__.
    """

    def __init__(self, children: list[Token] = None):
        """Creates the Container which contains all Containers.

        Note:
            This also parses the script into a list of Containers, which are then
            assigned as children.

        Args:
            children (list[Token], optional): All tokens belonging to a script. Defaults
                to None.
        """
        children = children or []

        super().__init__()
        box_stack = [Container()]

        for child in children:
            if child.type in [Atom.BOX_START, Atom.EXEC_START, Atom.IF_START]:
                if child.type is Atom.BOX_START:
                    b = Box()
                    box_stack.pop()  # remove newline from the stack
                elif child.type is Atom.EXEC_START:
                    b = ExecBlock()
                elif child.type is Atom.IF_START:
                    b = IfBlock()
                box_stack[-1].children.append(b)
                box_stack.append(box_stack[-1].children[-1])
            elif child.type in [Atom.BOX_END, Atom.EXEC_END, Atom.IF_END]:
                if child.type in [Atom.EXEC_END, Atom.IF_END]:
                    box_stack.pop()  # remove newline from stack
                box_stack.pop()
            elif child.type is Atom.NEWLINE:
                if isinstance(box_stack[-1], Line):
                    box_stack.pop()
                box_stack[-1].children.append(Line())
                box_stack.append(box_stack[-1].children[-1])
            else:
                box_stack[-1].children.append(child)

        self.children = [
            child for child in box_stack[0].children if not isinstance(child, Line)
        ]
