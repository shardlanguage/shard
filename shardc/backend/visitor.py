from shardc.frontend.tree.node import Node

class Visitor:
    def __init__(self, visit_prefix: str):
        self.visit_prefix = visit_prefix

    def generic_visit(self, node: Node) -> None:
        pass