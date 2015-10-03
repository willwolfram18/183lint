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
        # Treat traversal as post-order traversal
        for c in cursor.get_children():
            rubric._findOperators(c, operatorCursors)
        if isOperator(cursor):
            operatorCursors.append(cursor)

def _operatorSpacingCheckHelper(rubric, code, line, index, isCompound):
    if not isSpacedCorrectly(code, index, isCompound):
        spacingData = {
            'operator': code[index:index + 2] if isCompound else code[index:index + 1]
        }
        rubric._addError('OPERATOR_SPACING', line + 1, index + 1, spacingData)

def _evaluateBreakStatementsHelper(rubric, cursor, scopeStack):
    '''
    :type rubric: StyleRubric
    :type cursor: clang.cindex.Cursor
    :type scopeStack: list
    '''
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
    :type cursor: clang.cindex.Cursor
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
    :type code: string
    :type start: number
    :returns the index of the first operator encountered in code in the range [start, len(code))
    '''
    index = start
    while index < len(code) and code[index] not in '+=-*/%!><&|':
        index += 1
    return index

def isCompoundBinaryOperator(code, column):
    '''
    :type code: string
    :type column: number
    :returns True iff code[column:column + 2] is a a logical comparison operator
             (greater than equals, does not equal, logical AND, etc.), False otherwise
    '''
    return code[column:column + 2] in ['!=', '==', '<=', '>=', '&&', '||']

def isSpacedCorrectly(code, index, isCompound):
    '''
    :type code: str
    :type index: int
    :type isCompound: bool
    :return: bool
    '''
    postOffset = 2 if isCompound else 1
    # Checking spacing in front of operator
    if index - 1 >= 0 and index - 1 < len(code) and code[index - 1] not in [' ', '\n', '\r']:
        return False
    # Check spacing following operator
    elif index + postOffset < len(code) and code[index + postOffset] not in [' ', '\n', '\r']:
        return False
    return  True

def _findStaticAndDynamixCastsHelper(rubric, cursor, cursors):
    '''
    :type rubric: StyleRubric
    :type cursor: clang.cindex.Cursor
    :type cursors: list
    '''
    if rubric._cursorNotInFile(cursor):
        return
    for c in cursor.get_children():
        _findStaticAndDynamixCastsHelper(rubric, c, cursors)
    if cursor.kind == CursorKind.CXX_CONST_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_STATIC_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_DYNAMIC_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_REINTERPRET_CAST_EXPR:
        cursors.append(cursor)

def findStaticAndDynamicCasts(rubric, operatorLocationDict):
    '''
    :type rubric: StyleRubric
    :type operatorLocationDict: dict[int, set]
    '''
    castCursors = []
    _findStaticAndDynamixCastsHelper(rubric, rubric._clangCursor, castCursors)

    for c in castCursors:
        # Clang does line and column indexing by 1
        lineNumber = c.location.line - 1
        code = rubric._cleanLines.lines[lineNumber]

        if lineNumber not in operatorLocationDict:
            operatorLocationDict[lineNumber] = set()

        index = findOperatorStart(code, c.location.column - 1)
        while index in operatorLocationDict[lineNumber] and index < len(code):
            index = findOperatorStart(code, index + 1)
        if index < len(code) and code[index] == '<':
            # Add the opening angle bracket of static cast
            operatorLocationDict[lineNumber].add(index)
            index = findOperatorStart(code, index + 1)
            while index in operatorLocationDict[lineNumber] and index < len(code):
                index = findOperatorStart(code, index + 1)
            if index < len(code):
                assert code[index] == '>'
                operatorLocationDict[lineNumber].add(index)


