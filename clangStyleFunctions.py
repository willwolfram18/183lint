from clang.cindex import CursorKind
from clangStyleHelpers import isOperator

def evaluateOperatorSpacing(self):
    # Find all of the operators
    cursors = []
    self._findOperators(self._clangCursor, cursors)

