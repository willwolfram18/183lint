from clang.cindex import CursorKind

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

def isOperator(cursor):
    return cursor.kind == CursorKind.BINARY_OPERATOR or \
            cursor.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR or \
            cursor.kind == CursorKind.UNARY_OPERATOR or \
           ((cursor.displayname == 'operator<<' or cursor.displayname == 'operator>>') and \
               cursor.kind == CursorKind.UNEXPOSED_EXPR)

def findOperatorStart(code, start):
    '''
    Finds the first
    '''
    index = start
    while index < len(code) and code[index] not in '+=-*/%!><&|':
        index += 1
    return index

def isCompoundBinaryOperator(code, column):
    return code[column:column + 2] in ['!=', '==', '<=', '>=', '&&', '||']