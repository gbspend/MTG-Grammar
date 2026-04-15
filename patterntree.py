class Node:
    def __init__(self,s):
        self.s = s
        self.children = []
        self.count = 0
    
    def add(self,s2):
        for n in self.children:
            if n.s == s2:
                n.count += 1
                return n
        n = Node(s2)
        self.children.append(n)
        return n

class PatternTree:
    def __init__(self):
        self.root = Node("")
    
    def addToks(self, toks):
        curr = self.root
        for t in toks:
            curr = curr.add(t)