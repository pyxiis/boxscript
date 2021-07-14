class Container:
    def __init__(self):
        self.children = []
        self.closed = False
    
    def execute(self):
        raise NotImplementedError

class Block(Container):
    def execute(self):
        for child in self.children:
            r = child.execute()
        return r

class IfBlock(Block):
    pass

class ExecBlock(Block):
    pass

class Box(Container):
    def execute(self):
        conditional = any(child.isinstance(IfBlock) for child in self.children)
        if conditional:
            for child in self.children:
                value = child.execute()
                if child.isinstance(IfBlock) and not value:
                    return
            self.execute()
        else:
            for child in self.children:
                child.execute()
            
