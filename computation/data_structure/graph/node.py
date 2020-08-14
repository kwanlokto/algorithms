class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def __repr__(self):
        str_node = f"{self.value}"
        if len(self.children) == 1:
            str_node += f" -> {self.children[0]}"
        elif len(self.children) > 1:
            str_node += f" -> {[self.children]}"
        return str_node
