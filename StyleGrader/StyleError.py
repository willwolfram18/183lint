class StyleError(object):
    """
    Represents a style error in the student's code.
    """

    def __init__(self):
        self.lineNum = 0
        self.colNum = 0
        self.pointVal = 0
        self.label = 'ERROR'
        self.data = dict()
        self.message = ""

    def __init__(self, lineNum=0, colNum=0, points=0, label='ERROR', data={}):
        """
        Log the line number, type and point value of a specific error.
        :type points: int Weight of this error.
        :type label: str Key for response lookup in list_of_errors.
        :type line_num: int Line number of this error.
        :type column_num: int Column number of this error.
        :type data: dict Additional information about the error,
        """
        self.lineNum = lineNum
        self.colNum = colNum
        self.pointVal = points
        self.label = label
        self.data = data
        self._setMessage()


    def __eq__(self, other):
        return self.data == other.data and self.lineNum == other.lineNum and \
                self.colNum == other.colNum and self.message == other.message

    def __gt__(self, other):
        if self.lineNum > other.lineNum:
            return True
        elif self.lineNum == other.lineNum and self.colNum > other.colNum:
            return True
        else:
            return False

    def __str__(self):
        if not self.message:
            self._setMessage()
        return self.message

    def _setMessage(self):
        messages = {
            'UNARY_OPERATOR_SPACING': 'Incorrect spacing around the unary {} operator.'.format(self.data.get('operator')),
            'OPERATOR_SPACING': 'Incorrect spacing around {} operator.'.format(self.data.get('operator')),
            'GOTO': 'EECS 183 prohibits the use of goto statements.',
            'TERNARY_OPERATOR': 'EECS 183 advises against the use of the ternary operator (e.g. int x = foo() ? 1 : 2).',
            'LINE_LENGTH': 'Line exceeds 90 characters.',
            'COMPARISON_TO_BOOL': 'Do not do make comparisons with bool literals, such as == true.',
            'INFINITE_LOOP': 'Please do not use infinite loops such as while(true) or while(!false).',
            'UNNECESSARY_BREAK': 'EECS 183 prohibits the use of break inside of any loop.',
            'EXIT': 'Do not use exit()',
            'CONTINUE': 'Do not use continue',
            'BANNED_INCLUDE': 'You have included {0}, a library that we have prohibited.'.format(self.data.get("library")),
            'USING_TABS': 'One or more lines of code begins with the tab character. Please convert all lines to start with spaces.',
        }
        if self.label in messages:
            self.message = messages[self.label]
        else:
            self.message = '"{}" is not a supported label'.format(self.label)

    # def getErrorMessage(self, label):
    #     return {
    #         "USING_TABS": "Instead of tabs you must use spaces.  Fix and resubmit your code :).",
    #         "OPERATOR_SPACING": "Incorrect spacing around {}. If this is the unary + or - operator, you may ignore this error.".format(self.getData().get('operator')),
    #         "BLOCK_INDENTATION": "Incorrect indentation. Expected: {}, found: {}.".format(self.getData().get('expected'), self.getData().get('found')),
    #         "STATEMENTS_PER_LINE": "There should only be one command (statement) on each line.",
    #         "IF_ELSE_ERROR": "Every If-Else statement should have brackets.",
    #         "NON_CONST_GLOBAL": "You should never have a non-const global variable.",
    #         "FUNCTION_LENGTH_ERROR": "Your function is too long. Break it up into separate functions.",
    #         "LINE_WIDTH": "Line of {} characters exceeded the limit of 90.".format(self.getData().get('length')),
    #         "INT_FOR_BOOL": "You need to return true or false, instead of an actual number.",
    #         "MAGIC_NUMBER": "Store numbers in variables, so that you can give them meaningful names.",
    #         "BRACE_CONSISTENCY": "Your braces should be either Egyptian or block style, pick one.",
    #         "SPACING_ERROR": "Use tabs or spaces, not both.",
    #         "UNNECESSARY_BREAK": "Breaks should ONLY be used in switch statements. Fix your logic.",
    #         "GOTO": "Never use the goto function.",
    #         "DEFINE_STATEMENT": "While define statements have their applications, we do not allow them in EECS 183.",
    #         "EQUALS_TRUE": "It is stylistically preferred to use 'if (x)' instead of 'if (x == true)'.",
    #         "WHILE_TRUE": "It is almost always preferred to use an explicit conditional instead of 'while(true)'.",
    #         "TERNARY_OPERATOR": "The use of ternary expressions (e.g. return f(x) ? true : false) is discouraged in EECS 183.",
    #         "CONTINUE_STATEMENT": "While 'continue' is occasionally appropriate, we discourage its use in EECS 183.",
    #         "MAIN_SYNTAX": "Your declaration of main() does not adhere to conventional stylistic guidelines.",
    #         "STRINGSTREAM": "We disallow the use of stringstreams in this course to ensure mastery of other IO methods.",
    #         "UNNECESSARY_INCLUDE": "You have included a library we do not allow.",
    #         "FIRST_CHAR": "First character of a {} name must be capitalized. Expected: {}, found: {}.".format(self.getData().get("keyword"),
    #                                                                                                          self.getData().get("expected"),
    #                                                                                                          self.getData().get("found")),
    #         "OPERATOR_CONSISTENCY": "Your spacing around operators is inconsistent. Pick left, right or both for spacing and stick to it.",
    #         "POINTER_REFERENCE_CONSISTENCY": "Your use of spacing surrounding '*' and '&' is inconsistent.",
    #         "MISSING_RME": "{} is missing a complete RME.".format(self.getData().get("function")),
    #         "MIN_COMMENTS": "Potentially too few comments. Found {} {} of comments in {} {} of code.".format(self.getData().get("comments"),
    #                                                                                                         'line' if self.getData().get("comments") == 1 else 'lines',
    #                                                                                                         self.getData().get("lines"),
    #                                                                                                         'line' if self.getData().get("lines") == 1 else 'lines'),
    #         "DEFINITION_ABOVE_MAIN": "{} is implemented above main. Keep function definitions below main or in a separate .cpp file.".format(self.getData().get("function")),
    #         "FOR_LOOP_SEMICOLON_SPACING": "The loop on line {} doesn't have consistent spacing around its semicolons.".format(self.getData().get("line")),
    #     }[label]


