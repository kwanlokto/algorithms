class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parents = []

    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def add_parent(self, node):
        if isinstance(node, Node):
            self.parents.append(node)
