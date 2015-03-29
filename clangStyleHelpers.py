from clang.cindex import CursorKind

'''
Helper functions for the StyleRubric class
'''
def _cursorNotInFile(self, cursor):
        return cursor.location.file and \
               cursor.location.file.name != self._currentFilename

def _findOperators(self, cursor, operatorCursors):
        if self._cursorNotInFile(cursor):
            return
        if isOperator(cursor):
            operatorCursors.append(cursor)
        for c in cursor.get_children():
            self._findOperators(c, operatorCursors)


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
    if index - 1 >= 0 and code[index - 1] not in [' ', '\n', '\r']:
        return False
    elif index + postOffset < len(code) and code[index + postOffset] not in [' ', '\n', '\r']:
        return False
    return  True