class Node:
    def accept(self, visitor):
        func_name = f"visit_{self.__class__.__name__}"
        visit = getattr(visitor, func_name, visitor.generic_visit)
        return visit(self)