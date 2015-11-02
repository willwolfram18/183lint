from clang.cindex import CursorKind
from clangStyleHelpers import findOperatorStart, isCompoundBinaryOperator, \
        evaluateBreakStatementsHelper, findStaticAndDynamicCasts, cleanStringsAndChars, \
        lineBeginsWithSpaces, handleUnaryOperatorSpacing, checkOverloadedOperatorSpacing

def __dir__():
    return [evaluateOperatorSpacing, evaluateTernaryOperator, evaluateBreakStatements,
            evaluateContinueStatements, evaluateGotoStatments, evaluateWhileTrue,
            evaluateBoolLiteralComparison, evaluateLineLength, evaluateLibraries,
            evaluateUseOfTabs]

def evaluateOperatorSpacing(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that references an
    operator and is improperly spaced
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    # Find all of the operators
    cursors = []
    rubric._findOperators(rubric._clangCursor, cursors)

    # Maintain which operators on the line have already been checked
    operatorLocationDict = {}
    findStaticAndDynamicCasts(rubric, operatorLocationDict)
    for c in cursors:
        # Clang's line and column numbers are 1-indexed, need -1 for zero index
        lineNumber = c.location.line - 1
        code = rubric.getLineOfCode(lineNumber)
        columnLenDiff = len(code)
        code, colDeleteLocation = cleanStringsAndChars(code)
        # Removed characters from the line, causes column to shift
        # Didn't make any deletions or shift is after the current column
        if colDeleteLocation == -1 or colDeleteLocation > c.location.column - 1:
            columnLenDiff = 0
        else:
            columnLenDiff = columnLenDiff - len(code)

        # Create the set if we haven't already
        if lineNumber not in operatorLocationDict:
            operatorLocationDict[lineNumber] = set()

        # Keep looking for an operator until we've found one not in the set
        index = findOperatorStart(code, c.location.column - 1 - columnLenDiff)
        while index in operatorLocationDict[lineNumber] and index < len(code):
            index = findOperatorStart(code, index + 1)
        if index < len(code):
            operatorLocationDict[lineNumber].add(index)

            if c.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
                operatorLocationDict[lineNumber].add(index + 1) # Operator spans 2 locations, add the second part of the operator

                # handle special case where using binary shift assignment
                if index + 2 < len(code) and code[index:index+3] in ['<<=', '>>=']:
                    operatorLocationDict[lineNumber].add(index + 3)
                    if (index - 1 >= 0 and code[index - 1] not in ['\n', '\r', ' ']) or \
                        (index + 3 < len(code) and code[index + 3] not in ['\n', '\r', ' ']):
                        spacingData = {
                            'operator': code[index:index+3]
                        }
                        rubric._addError('OPERATOR_SPACING', lineNumber + 1, index + 1, spacingData)
                else:
                    rubric.checkOperatorSpacing(code, lineNumber, index, True)
            elif c.kind == CursorKind.BINARY_OPERATOR:
                if isCompoundBinaryOperator(code, index):
                    operatorLocationDict[lineNumber].add(index + 1) # Operator spans 2 locations, add the second part of the operator
                    if code[index:index + 3] == '->*': # Ignore the ->* operator
                        operatorLocationDict[lineNumber].add(index + 2)
                    elif code[index:index + 2] != '->': # Ignore the -> operator
                        rubric.checkOperatorSpacing(code, lineNumber, index, True)
                else:
                    rubric.checkOperatorSpacing(code, lineNumber, index, False)
            elif c.kind == CursorKind.UNARY_OPERATOR:
                if index + 1 < len(code) and code[index] == code[index + 1]:
                    # No rules for the ++ and -- operators, just skip it
                    operatorLocationDict[lineNumber].add(index + 1)
                else:
                   handleUnaryOperatorSpacing(rubric, code, lineNumber, index)
            else: # operator overload functions
                checkOverloadedOperatorSpacing(rubric, c, code, index, lineNumber, operatorLocationDict)

def evaluateTernaryOperator(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is a
    ternary operator
    :type rubric: StyleGrader.StyleRubric
    :type cursor:
    :return:
    '''
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.CONDITIONAL_OPERATOR:
        rubric._addError('TERNARY_OPERATOR', cursor.location.line, cursor.location.column)
    for c in cursor.get_children():
        evaluateTernaryOperator(rubric, c)

def evaluateBreakStatements(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is a break
    statement outside of a switch statement
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    scopeStack = []
    evaluateBreakStatementsHelper(rubric, cursor, scopeStack)

def evaluateContinueStatements(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is a Continue statement
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.CONTINUE_STMT:
        rubric._addError('CONTINUE', cursor.location.line, cursor.location.column)
    for c in cursor.get_children():
        evaluateContinueStatements(rubric, c)

def evaluateGotoStatments(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is a goto statement
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.GOTO_STMT:
        rubric._addError('GOTO', cursor.location.line, cursor.location.column)
    for c in cursor.get_children():
        evaluateGotoStatments(rubric, c)

def evaluateWhileTrue(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is a continuous
    loop structure (while(true) or while(!false) for example)
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.DO_STMT or cursor.kind == CursorKind.WHILE_STMT:
        loopConditionCursor = None
        if cursor.kind == CursorKind.DO_STMT:
            loopConditionCursor = [x for x in cursor.get_children()][1]
        else:
            loopConditionCursor = [x for x in cursor.get_children()][0]
        assert loopConditionCursor

        if loopConditionCursor.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
            rubric._addError('INFINITE_LOOP', loopConditionCursor.location.line, loopConditionCursor.location.column)
        elif loopConditionCursor.kind == CursorKind.UNARY_OPERATOR:
            # Found unary NOT operator, check if its first child is a literal bool
            child = [x for x in loopConditionCursor.get_children()][0]
            if child.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
                rubric._addError('INFINITE_LOOP', loopConditionCursor.location.line, loopConditionCursor.location.column)
    for c in cursor.get_children():
        evaluateWhileTrue(rubric, c)

def evaluateBoolLiteralComparison(rubric, cursor):
    '''
    Adds an error to the style rubric for each cursor in the AST that is pointing
    to an operator that is making a direct comparison to a bool literal (x == true
    for example)
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    if rubric._cursorNotInFile(cursor):
        return
    if cursor.kind == CursorKind.BINARY_OPERATOR:
        # cursor lines are 1 indexed, need -1 for correct array offset
        code = rubric.getLineOfCode(cursor.location.line - 1)
        index = findOperatorStart(code, cursor.location.column)
        if code[index:index+2] in ['==', '!=']:
            # Evaluate the children of the operator
            for child in cursor.get_children():
                if child.kind == CursorKind.UNEXPOSED_EXPR:
                    # AST does implicit cast (unexposed expression in Python) before
                    # listing bool literal, therefore grab immediate child
                    operand = [x for x in child.get_children()][0]
                    if operand.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
                        rubric._addError("COMPARISON_TO_BOOL", cursor.location.line, cursor.location.column)

    for c in cursor.get_children():
        evaluateBoolLiteralComparison(rubric, c)

def evaluateLineLength(rubric, cursor):
    '''
    Adds an error to the style rubric for each line of code that is longer than
    the rubric's max line length
    :type rubric:
    :type cursor:
    '''
    # Use safelyOpenFile because we want to look for lines with comments
    # included for line length
    data = rubric._safelyOpenFile()
    if data is None:
        return
    lineNum = 0
    for line in data:
        lineNum += 1
        if len(line) == 0: 
            continue
        # Remove the return character at the end of the line
        if line[-1] in ['\n', '\r']: 
            line = line[:-1]
        if len(line) > rubric._maxLineLength: 
            rubric._addError('LINE_LENGTH', lineNum, rubric._maxLineLength + 1)

def evaluateLibraries(rubric, cursor):
    '''
    Adds an error to the style rubric for each library that is included in the current
    file that is part of the rubric's prohibited libraries
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    for lib in rubric._translationUnit.get_includes():
        # Library name is last part of file name path
        libName = lib.location.file.name.split('/')[-1]
        if libName in rubric._prohibitedLibs and libName not in rubric._foundLibs:
            rubric._foundLibs.append(libName)
            rubric._addError('BANNED_INCLUDE', 1, 1, {'library': libName})
        if (libName == 'stdlib.h' or libName == 'cstdlib') and not rubric._stdLib:
            rubric._stdLib = True

def evaluateUseOfTabs(rubric, cursor):
    '''
    Adds an error to the style rubric if any line in the current file starts
    with tabs instead of 0 or more spaces
    :type rubric: StyleGrader.StyleRubric
    :type cursor: clang.cindex.Cursor
    '''
    for line in rubric.getCode():
        if not lineBeginsWithSpaces(line):
            rubric._addError('USING_TABS', 0, 0)
            break