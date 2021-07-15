from lang.lex import Atom, Token

class Container:
    def __init__(self, children: list = None):
        self.children = children or []

    def execute(self):
        r = 0
        for child in self.children:
            r = child.execute()
        return r


class Block(Container):
    pass


class IfBlock(Block):
    pass


class ExecBlock(Block):
    pass


class Box(Container):
    def execute(self):
        conditional = any(isinstance(child, IfBlock) for child in self.children)
        if conditional:
            for child in self.children:
                value = child.execute()
                if isinstance(child, IfBlock) and not value:
                    return
            self.execute()
        else:
            for child in self.children:
                child.execute()

class Line(Container):
    def execute(self):
        # we only execute the first child, because each line should only contain 1 child
        # all other tokens should be grandchildren
        return self.children[0].execute()        


class Script(Container):
    def __init__(self, children: list = []):
        super().__init__()
        box_stack = [Container()]
        
        for child in children:
            if child.type in [Atom.BOX_START, Atom.EXEC_START, Atom.IF_START]:
                if child.type is Atom.BOX_START:
                    b = Box()
                    box_stack.pop() # remove newline from the stack
                elif child.type is Atom.EXEC_START:
                    b = ExecBlock()
                elif child.type is Atom.IF_START:
                    b = IfBlock()
                box_stack[-1].children.append(b)
                box_stack.append(box_stack[-1].children[-1])
            elif child.type in [Atom.BOX_END, Atom.EXEC_END, Atom.IF_END]:
                if child.type in [Atom.EXEC_END, Atom.IF_END]:
                    box_stack.pop() # remove newline from stack
                box_stack.pop()
            elif child.type is Atom.NEWLINE:
                if isinstance(box_stack[-1], Line):
                    box_stack.pop()
                box_stack[-1].children.append(Line())
                box_stack.append(box_stack[-1].children[-1])
            else:
                box_stack[-1].children.append(child)

        self.children = [child for child in box_stack[0].children if not isinstance(child, Line)]
