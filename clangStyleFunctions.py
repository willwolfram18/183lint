from clang.cindex import CursorKind
from clangStyleHelpers import findOperatorStart, isCompoundBinaryOperator, \
        _evaluateBreakStatementsHelper

def __dir__():
    return [evaluateOperatorSpacing, evaluateTernaryOperator, evalueBreakStatements,
            evaluateContinueStatements]

def evaluateOperatorSpacing(rubric, cursor):
    # Find all of the operators
    cursors = []
    rubric._findOperators(rubric._clangCursor, cursors)

    # Maintain where we will start next operator search on that line
    nextStartOfLine = {}
    for c in cursors:
        # Clang's line and column numbers are 1-indexed, need -1 for zero index
        lineNumber = c.location.line - 1
        code = rubric._cleanLines.lines[lineNumber]

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
            rubric._operatorSpacingCheckHelper(code, lineNumber, index, True)
        elif c.kind == CursorKind.BINARY_OPERATOR:
            if isCompoundBinaryOperator(code, index):
                nextStartOfLine[lineNumber] += 1 # Operator spans 2 locations, move ahead one more
                rubric._operatorSpacingCheckHelper(code, lineNumber, index, True)
            else:
                rubric._operatorSpacingCheckHelper(code, lineNumber, index, False)
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
                    rubric._addError('UNARY_OPERATOR_SPACING', lineNumber + 1, index + 1, spacingData)
        else: # operator>> and operator<<
            rubric._operatorSpacingCheckHelper(code, lineNumber, index, True)

def evaluateTernaryOperator(rubric, cursor):
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.CONDITIONAL_OPERATOR:
        rubric._addError('TERNARY_OPERATOR', cursor.location.line, cursor.location.column)
    for c in cursor.get_children():
        evaluateTernaryOperator(rubric, c)

def evalueBreakStatements(rubric, cursor):
    scopeStack = []
    _evaluateBreakStatementsHelper(rubric, cursor, scopeStack)

def evaluateContinueStatements(rubric, cursor):
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.CONTINUE_STMT:
        rubric._addError('CONTINUE', cursor.location.line, cursor.location.column)
    for c in cursor.get_children():
        evaluateContinueStatements(rubric, c)