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
            # Save the next column
            nextStartOfLine[lineNumber] = c.location.column - 1
        elif nextStartOfLine[lineNumber] < c.location.column - 1:
            # Move ahead to the greater column
            nextStartOfLine[lineNumber] = c.location.column - 1

        index = findOperatorStart(code, nextStartOfLine[lineNumber])
        nextStartOfLine[lineNumber] = index + 1

        if c.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
            nextStartOfLine[lineNumber] += 1 # Operator spans 2 locations, move ahead one more
            self._operatorSpacingCheckHelper(code, lineNumber, index, True)
        elif c.kind == CursorKind.BINARY_OPERATOR:
            if isCompoundBinaryOperator(code, index):
                nextStartOfLine[lineNumber] += 1 # Operator spans 2 locations, move ahead one more
                self._operatorSpacingCheckHelper(code, lineNumber, index, True)
            else:
                self._operatorSpacingCheckHelper(code, lineNumber, index, False)
        elif c.kind == CursorKind.UNARY_OPERATOR:
            if index + 1 < len(code) and code[index] == code[index + 1]:
                # No rules for the ++ and -- operators, just skip it
                nextStartOfLine[lineNumber] += 1
            else:
                # Check for white space or ( in front, and no whitespace behind it
                if (index - 1 >= 0 and code[index - 1] not in [' ', '\n', '\r', '(']) or \
                    (index + 1 < len(code) and code[index + 1] in [' ', '\n', '\r']):
                    spacingData = {
                        'operator': code[index:index + 1],
                    }
                    self._addError('UNARY_OPERATOR_SPACING', lineNumber + 1, index + 1, spacingData)
        else: # operator>> and operator<<
            self._operatorSpacingCheckHelper(code, lineNumber, index, True)

