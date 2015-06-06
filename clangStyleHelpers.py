from clang.cindex import CursorKind

'''
Helper functions for the StyleRubric class
'''
def _cursorNotInFile(rubric, cursor):
        return cursor.location.file and \
               cursor.location.file.name != rubric._currentFilename

def _findOperators(rubric, cursor, operatorCursors):
        if rubric._cursorNotInFile(cursor):
            return
        if isOperator(cursor):
            operatorCursors.append(cursor)
        for c in cursor.get_children():
            rubric._findOperators(c, operatorCursors)

def _operatorSpacingCheckHelper(rubric, code, line, index, isCompound):
    if not isSpacedCorrectly(code, index, isCompound):
        spacingData = {
            'operator': code[index:index + 2] if isCompound else code[index:index + 1]
        }
        rubric._addError('OPERATOR_SPACING', line + 1, index + 1, spacingData)

def _evaluateBreakStatementsHelper(rubric, cursor, scopeStack):
    if rubric._cursorNotInFile(cursor):
        return

    addedScope = False
    if cursor.kind == CursorKind.SWITCH_STMT:
        scopeStack.append('SWITCH')
        addedScope = True
    elif cursor.kind == CursorKind.FOR_STMT or \
        cursor.kind == CursorKind.WHILE_STMT or \
        cursor.kind == CursorKind.DO_STMT:
        scopeStack.append('LOOP')
        addedScope = True
    elif cursor.kind == CursorKind.BREAK_STMT:
        if len(scopeStack) == 0 or scopeStack[-1] != 'SWITCH':
            rubric._addError('UNNECESSARY_BREAK', cursor.location.line, cursor.location.column)

    for c in cursor.get_children():
        _evaluateBreakStatementsHelper(rubric, c, scopeStack)
    if addedScope:
        scopeStack.pop()

'''
General helper functions
'''
def isOperator(cursor):
    '''
    :parameter cursor: object of type clang.cindex.Cursor
    :returns True iff cursor is a Binary, Compound Assignement, Unary, or output/input
             operator, False otherwise
    '''
    return cursor.kind == CursorKind.BINARY_OPERATOR or \
            cursor.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR or \
            cursor.kind == CursorKind.UNARY_OPERATOR or \
            ((cursor.displayname == 'operator<<' or cursor.displayname == 'operator>>') and \
               cursor.kind == CursorKind.UNEXPOSED_EXPR)

def findOperatorStart(code, start):
    '''
    :parameter code: string
    :parameter start: number
    :returns the index of the first operator encountered in code in the range [start, len(code))
    '''
    index = start
    while index < len(code) and code[index] not in '+=-*/%!><&|':
        index += 1
    return index

def isCompoundBinaryOperator(code, column):
    '''
    :parameter code: string
    :parameter column: number
    :returns True iff code[column:column + 2] is a a logical comparison operator
             (greater than equals, does not equal, logical AND, etc.), False otherwise
    '''
    return code[column:column + 2] in ['!=', '==', '<=', '>=', '&&', '||']

def isSpacedCorrectly(code, index, isCompound):
    postOffset = 2 if isCompound else 1
    # Checking spacing in front of operator
    if index - 1 >= 0 and code[index - 1] not in [' ', '\n', '\r']:
        return False
    # Check spacing following operator
    elif index + postOffset < len(code) and code[index + postOffset] not in [' ', '\n', '\r']:
        return False
    return  True

