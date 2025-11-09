from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shardc.backend.visitor import Visitor

class Node:
    def accept(self, visitor: 'Visitor'):
        func_name = f"{visitor.visit_prefix}_{self.__class__.__name__}"
        visit = getattr(visitor, func_name, visitor.generic_visit)
        return visit(self)