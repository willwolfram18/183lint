from clang.cindex import CursorKind
from clangStyleHelpers import findOperatorStart, isSpacedCorrectly, isCompoundBinaryOperator

def evaluateOperatorSpacing(self):
    # Find all of the operators
    cursors = []
    self._findOperators(self._clangCursor, cursors)

    # Maintain where we will start next operator search on that line
    nextStartOfLine = {}
    for c in cursors:
        # Clang's line and column numbers are 1-indexed, need -1 for zero index
        lineNumber = c.location.line - 1
        code = self._cleanLines.lines[lineNumber]

        if lineNumber not in nextStartOfLine:
            nextStartOfLine[lineNumber] = c.location.column - 1
        index = findOperatorStart(code, nextStartOfLine[lineNumber])
        nextStartOfLine[lineNumber] = index + 1

        if c.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
            nextStartOfLine[lineNumber] += 1 # Operator spans 2 locations, move ahead one more
            if not isSpacedCorrectly(code, index, True):
                pass
        elif c.kind == CursorKind.BINARY_OPERATOR:
            if isCompoundBinaryOperator(code, index):
                nextStartOfLine[lineNumber] += 1 # Operator spans 2 locations, move ahead one more
            else:
                pass
        elif c.kind == CursorKind.UNARY_OPERATOR:
            if index + 1 < len(code) and code[index] == code[index + 1]:
                nextStartOfLine[lineNumber] += 1
            else:
                pass
        else: # operator>> and operator<<
            pass

