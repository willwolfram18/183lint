import os
import unittest
from StyleGrader import StyleError, StyleRubric

def assertionMessage(expected, found):
    return 'Expected {} errors, found {}.'.format(expected, found)

def errorTypeMessage(expected, errType, found):
    return 'Expected {} {} errors, found {}.'.format(expected, errType, found)

def checkTotalErrors(test, rubric, fileName, numExpected):
    '''

    :type test: RegressionTest
    :type rubric: StyleRubric
    :type numExpected: int
    '''
    errorDict = rubric.generateReport()
    numFound = len(errorDict[fileName])
    test.assertEqual(numFound, numExpected, assertionMessage(numExpected, numFound))

def checkErrorTypes(test, errorDict, expectedErrorsDict, allowedErrorTypes):
    '''

    :type test: RegressionTest
    :type errorDict: dict[str, int]
    :type expectedErrorsDict: dict[str, int]
    :type allowedErrorTypes: list[str]
    '''
    for errType in StyleError.ErrorTypes:
        if errType in allowedErrorTypes:
            errorsExpected = expectedErrorsDict[errType]

            # Check that error type does exist in dictionary
            test.assertTrue(errType in errorDict,
                                      errorTypeMessage(errorsExpected, errType, 'none'))
            errorsFound = errorDict[errType]
            test.assertEqual(errorsFound, errorsExpected,
                             errorTypeMessage(errorsExpected, errType, errorsFound))
        else:
            test.assertFalse(errType in errorDict, errorTypeMessage(0, errType, 'at least 1'))

class RegressionTest(unittest.TestCase):

    def test_BoolComp(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 10,
            'COMPARISON_TO_BOOL': 10,
        }
        allowedErrTypes = ['COMPARISON_TO_BOOL']

        fileName = os.path.join('test', 'bool_comp.cpp')
        self.assertTrue(os.path.exists(fileName), 'Test file "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, 'bool_comp.cpp', expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_OperatorSpacingBad(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 38,
            'OPERATOR_SPACING': 35,
            'UNARY_OPERATOR_SPACING': 1,
            'COMPARISON_TO_BOOL': 2
        }
        allowedErrTypes = ['OPERATOR_SPACING', 'UNARY_OPERATOR_SPACING', 'COMPARISON_TO_BOOL']

        fileName = os.path.join('test', 'operator_spacing_bad.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_OperatorSpacingGood(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 2,
            'COMPARISON_TO_BOOL': 2
        }
        allowedErrTypes = ['COMPARISON_TO_BOOL']

        fileName = os.path.join('test', 'operator_spacing_good.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_OperatorSpacingOverload(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 6,
            'OPERATOR_SPACING': 5,
            'UNARY_OPERATOR_SPACING': 1,
        }
        allowedErrTypes = ['OPERATOR_SPACING', 'UNARY_OPERATOR_SPACING']

        fileName = os.path.join('test', 'operator_overload_myint.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_BreakStatements(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 5,
            'UNNECESSARY_BREAK': 3,
            'INFINITE_LOOP': 2,
        }
        allowedErrTypes = ['UNNECESSARY_BREAK', 'INFINITE_LOOP']

        fileName = os.path.join('test', 'break_bad.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_ContinueBad(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 4,
            'CONTINUE': 3,
            'INFINITE_LOOP': 1,
        }
        allowedErrTypes = ['CONTINUE', 'INFINITE_LOOP']

        fileName = os.path.join('test', 'continue_bad.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_ContinueGood(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 0,
        }
        allowedErrTypes = []

        fileName = os.path.join('test', 'continue_good.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_GotoBad(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 1,
            'GOTO': 1,
        }
        allowedErrTypes = ['GOTO']

        fileName = os.path.join('test', 'goto_bad.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_GotoGood(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 0
        }
        allowedErrTypes = []

        fileName = os.path.join('test', 'goto_good.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_InfiniteLoopBad(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 6,
            'INFINITE_LOOP': 6
        }
        allowedErrTypes = ['INFINITE_LOOP']

        fileName = os.path.join('test', 'while_true_bad.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_InfiniteLoopGood(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 0
        }
        allowedErrTypes = []

        fileName = os.path.join('test', 'while_true_good.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_LineLength(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 2,
            'LINE_LENGTH': 2
        }
        allowedErrTypes = ['LINE_LENGTH']

        fileName = os.path.join('test', 'line_length.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

    def test_Indentation(self):
        rubric = StyleRubric()
        expectedErrors = {
            'total': 1,
            'USING_TABS': 1
        }
        allowedErrTypes = ['USING_TABS']

        fileName = os.path.join('test', 'tab_indents.cpp')
        self.assertTrue(os.path.exists(fileName), 'File "{}" does not exist.'.format(fileName))

        rubric.gradeFile(fileName)
        checkTotalErrors(self, rubric, os.path.split(fileName)[1], expectedErrors['total'])
        checkErrorTypes(self, rubric._errorTypes, expectedErrors, allowedErrTypes)

if __name__ == '__main__':
    unittest.main()