from clang.cindex import CursorKind
import re

def evaluateBreakStatementsHelper(rubric, cursor, scopeStack):
    '''
    Reads the Clang syntax tree, checking for break statements outside of switch
    statements. Scope stack is used to maintain which type of control context the
    cursor is currently in (only tracks switch statements, or loop controls)
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    :type scopeStack: list[str]
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
        evaluateBreakStatementsHelper(rubric, c, scopeStack)
    if addedScope:
        scopeStack.pop()

def isOperator(cursor):
    '''
    Checks to see if the provided cursor is an operator cursor. Returns true if the
    cursor's kind is BINARY_OPERATOR, COMPOUND_ASSIGNMENT_OPERATOR, UNARY_OPERATOR,
    or is a function overload for a C++ class
    :type cursor: clang.cindex.Cursor
    :returns bool
    '''
    return cursor.kind == CursorKind.BINARY_OPERATOR or \
            cursor.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR or \
            cursor.kind == CursorKind.UNARY_OPERATOR or \
           ('operator' in cursor.displayname and cursor.kind == CursorKind.UNEXPOSED_EXPR)
            # ((cursor.displayname == 'operator<<' or cursor.displayname == 'operator>>') and \
            #    cursor.kind == CursorKind.UNEXPOSED_EXPR)

def findOperatorStart(code, start):
    '''
    Finds the index of the first operator encountered in code in the range
    [start, len(code)). If no operator is found, returns the len(code)
    :type code: str
    :type start: number
    :returns int
    '''
    index = start
    while index < len(code) and code[index] not in '+=-*/%!><&|':
        index += 1
    return index

def isCompoundBinaryOperator(code, column):
    '''
    Checks to see if the operator located at column is a two-character operator (e.g.
    ==, !=, >=, etc.)
    :type code: str
    :type column: int
    :returns bool
    '''
    return code[column:column + 2] in ['!=', '==', '<=', '>=', '&&', '||', '->']

def handleUnaryOperatorSpacing(rubric, code, lineNum, index):
    '''

    :type rubric: StyleGrader.StyleRubric
    :type code: str
    :type lineNum: int
    :type index: int
    '''
    # Check for white space or ( in front, and no whitespace behind it
    if (index - 1 >= 0 and code[index - 1] not in ['(', ' ', '\n', '\r']) or \
        (index + 1 < len(code) and code[index] in [' ', '\n', '\r']):
        spacingData = {
            'operator': code[index:index+1]
        }
        rubric._addError('UNARY_OPERATOR_SPACING', lineNum + 1, index + 1, spacingData)

def isSpacedCorrectly(code, index, isCompound):
    '''
    Checks to see if the operator has the appropriate white space characters preceding
    and following it
    :type code: str
    :type index: int
    :type isCompound: bool
    :return: bool
    '''
    allowedSurroundingChars = [' ', '\n', '\r']
    postOffset = 2 if isCompound else 1
    # Checking spacing in front of operator
    if index - 1 >= 0 and index - 1 < len(code) and code[index - 1] not in allowedSurroundingChars:
        return False
    # Check spacing following operator
    elif index + postOffset < len(code) and code[index + postOffset] not in allowedSurroundingChars:
        return False
    return True

def _findStaticAndDynamicCastsHelper(rubric, cursor, cursors):
    '''
    Looks through the Clang AST, placing any static or dynamic cast cursors into
    the cursors list
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    :type cursors: list[clang.cindex.Cursor]
    '''
    if rubric._cursorNotInFile(cursor):
        return
    for c in cursor.get_children():
        _findStaticAndDynamicCastsHelper(rubric, c, cursors)
    if cursor.kind == CursorKind.CXX_CONST_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_STATIC_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_DYNAMIC_CAST_EXPR or \
        cursor.kind == CursorKind.CXX_REINTERPRET_CAST_EXPR:
        cursors.append(cursor)

def findStaticAndDynamicCasts(rubric, operatorLocationDict):
    '''
    Gathers all static and dynamic cast cursors in the file, and checks to see
    if they follow the C++ style casts (e.g. static_cast<type_t>(operand)), and adds
    the angle brackets to the operatorLocationDict to prevent them being treated
    as operators
    :type rubric: StyleGrader.StyleRubric
    :type operatorLocationDict: dict[int, set[int]]
    '''
    castCursors = []
    _findStaticAndDynamicCastsHelper(rubric, rubric._clangCursor, castCursors)

    for c in castCursors:
        # Clang does line and column indexing by 1
        lineNumber = c.location.line - 1
        code = rubric.getLineOfCode(lineNumber)

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

def cleanStringsAndChars(code):
    '''
    Cleans the provided string of any literal characters and strings. For example,
    converts the line "Hello world!"; to "";
    :type code: str
    :return: str,int
    '''
    charPattern = re.compile("'.+?'", re.DOTALL)
    stringPattern = re.compile('".+?"', re.DOTALL)

    # Store location of first erase, use later to see if column has shifted
    findIndex = None
    # Remove escaped single and double quote characters
    firstReplace = code.find("\\'")
    code = code.replace("\\'", '')

    # Iterate over all matched literal chars
    results = charPattern.findall(code)
    for match in results:
        findIndex = code.find(match)
        if firstReplace == -1 or findIndex < firstReplace:
            firstReplace = findIndex
        code = code.replace(match, "''")

    # Iterate over all matched literal strings
    findIndex = code.find('\\"')
    if firstReplace == -1 or\
        (findIndex != -1 and findIndex < firstReplace):
        firstReplace = findIndex
    code = code.replace('\\"', '')
    results = stringPattern.findall(code)
    for match in results:
        findIndex = code.find(match)
        if firstReplace == -1 or findIndex < firstReplace:
            firstReplace = findIndex
        code = code.replace(match, '""')
    return code, firstReplace

def lineBeginsWithSpaces(code):
    '''
    Checks to see if the provided string starts with 0 or more spaces and doesn't
    start with tabs.
    :type code: str
    :return: bool
    '''
    startsWithSpace = re.compile('^ *')
    startsWithTab = re.compile('^\t+')
    return not startsWithTab.match(code) and startsWithSpace.match(code)

def checkOverloadedOperatorSpacing(rubric, cursor, code, index, lineNum, operatorLocationDict):
    '''
    Performs operator spacing evaluation on overloaded operators for a C++ class
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    :type code: string
    :type index: int
    :type lineNum: int
    :type operatorLocationDict: dict[int, set[int]]
    '''
    # Sanity check that line number is in operator dict
    if lineNum not in operatorLocationDict:
        operatorLocationDict[lineNum] = set()
    if index not in operatorLocationDict[lineNum]:
        operatorLocationDict.add(index)

    ignoredOperators = ['++', '--', '->', '->*', '()', '[]', ',']
    operator = cursor.displayname.replace('operator', '')
    if operator in ignoredOperators:
        # Make sure to add operator locations for subsequent operator checks
        if operator in ['++', '--', '->']:
            operatorLocationDict[lineNum].add(index + 1)
        elif operator == '->*':
            operatorLocationDict[lineNum].add(index + 1)
            operatorLocationDict[lineNum].add(index + 2)
        return

    # Binary operators that have two characters
    binaryTwoSpace = ['+=', '-=', '*=', '/=', '%=', '^=', '&=', '|=', '>>', '<<',
                      '==', '!=', '<=', '>=', '&&', '||']
    # Binary operators that have one character
    binarySingleSpace = ['<', '>', '=', '/', '%', '&', '|']
    # Guaranteed unary operators
    unaryOperators = ['!', '~']
    # Binary or unary operators
    binaryOrUnary = ['+', '-', '*']

    if operator in binaryTwoSpace:
        operatorLocationDict[lineNum].add(index + 1)
        rubric.checkOperatorSpacing(code, lineNum, index, True)
    elif operator in ['>>=', '<<=']:
        operatorLocationDict[lineNum].add(index + 1)
        operatorLocationDict[lineNum].add(index + 2)
        if (index - 1 >= 0 and code[index - 1] not in ['\n', '\r', ' ']) or \
                (index + 3 < len(code) and code[index + 3] not in ['\n', '\r', ' ']):
            spacingData = {
                'operator': code[index:index+3]
            }
            rubric._addError('OPERATOR_SPACING', lineNum + 1, index + 1, spacingData)
    elif operator in binarySingleSpace:
        rubric.checkOperatorSpacing(code, lineNum, index, False)
    elif operator in unaryOperators:
       handleUnaryOperatorSpacing(rubric, code, lineNum, index)
    elif operator in binaryOrUnary:
        unaryExpressions = [
            re.compile('.+ \(\*\)\(\)'), # matches type_t (*)() member func
            re.compile('.+ \(\*\)\(.\)') # matches type_t (*)(type_t) friend func
        ]
        # Typical convention is binary expressions as friend functions with 2 parameters
        # to the function
        binaryExpression = re.compile('.+ \(\*\)\(.+\, .+\)'), # matches type_t (*)(type_x, type_y)
        isUnary = False
        for expr in unaryExpressions:
            if expr.match(cursor.type.spelling):
                handleUnaryOperatorSpacing(rubric, code, lineNum, index)
                isUnary = True
                break
        if not isUnary and binaryExpression.match(code):
            rubric.checkOperatorSpacing(code, lineNum, index, False)