import unittest
from StyleRubric import StyleRubric

def assertionMessage(expected, found, errorList=[]):
    if expected == 0:
        return 'Should be 0 errors total, found {}.'.format(found)
    # Create a comma separated string
    errorString = errorList[0]
    if len(errorList) > 1:
        for i in range(1, len(errorList) - 1):
            errorString += ',' + errorList[i]
        errorString += ', and ' + errorList[-1]
    return 'Should be {} errors total ({}), found {}.'.format(expected, errorString, found)

class RegressionTest(unittest.TestCase):

    def testOperatorSpacing(self):
        rubric = StyleRubric()

        # TODO: Find way to grab test file paths via os.path
        badTestName = 'test/operator_spacing_bad.cpp'
        rubric.gradeFile(badTestName)
        self.assertEqual(rubric._errorTypes['OPERATOR_SPACING'], 35)
        self.assertEqual(rubric._errorTypes['UNARY_OPERATOR_SPACING'], 1)
        self.assertEqual(rubric._totalErrors, 38, assertionMessage(38, rubric._totalErrors, ['36 operator spacing', '2 == true']))

        rubric.resetRubric()
        goodTestName = 'test/operator_spacing_good.cpp'
        rubric.gradeFile(goodTestName)
        self.assertEqual('OPERATOR_SPACING' not in rubric._errorTypes, True)
        self.assertEqual('UNARY_OPERATOR_SPACING' not in rubric._errorTypes, True)
        self.assertEqual(rubric._totalErrors, 2, assertionMessage(2, rubric._totalErrors, ['2 == true']))


    def testBreakStatements(self):
        rubric = StyleRubric()

        # TODO: Find file paths
        badTestName = 'test/break_bad.cpp'
        rubric.gradeFile(badTestName)
        self.assertEqual(rubric._errorTypes['UNNECESSARY_BREAK'], 3)
        self.assertEqual(rubric._totalErrors, 5, assertionMessage(4, rubric._totalErrors, ['3 unnecessary breaks', '2 == true']))

        rubric.resetRubric()
        goodTestName = 'test/operator_spacing_good.cpp'
        rubric.gradeFile(goodTestName)
        self.assertEqual('UNNECESSARY_BREAK' not in rubric._errorTypes, True)
        self.assertEqual(rubric._totalErrors, 2, assertionMessage(2, rubric._totalErrors, ['2 == true']))

    def testContinueStatements(self):
        rubric = StyleRubric()

        # TODO: Find the file paths
        badTestName = 'test/continue_bad.cpp'
        rubric.gradeFile(badTestName)
        self.assertEqual(rubric._errorTypes['CONTINUE'], 3)
        self.assertEqual(rubric._totalErrors, 4, assertionMessage(4, rubric._totalErrors, ['3 continues', '1 infinite loop']))

        rubric.resetRubric()
        goodTestName = 'test/continue_good.cpp'
        rubric.gradeFile(goodTestName)
        self.assertEqual('CONTINUE' not in rubric._errorTypes, True)
        self.assertEqual(rubric._totalErrors, 0, assertionMessage(0, rubric._totalErrors))

    def testGotoStatements(self):
        pass

    def testInfiniteLoop(self):
        pass

    def testBoolComparison(self):
        pass

    def testCompileError(self):
        pass

if __name__ == '__main__':
    unittest.main()