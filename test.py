from StyleRubric import StyleRubric

s = StyleRubric()
s.gradeFile('test/operator_spacing_bad.cpp')
for filename, errors in s._fileErrors.iteritems():
    if len(errors) == 0:
        print 'No errors found :D'
    else:
        for e in errors:
            print '{0}:{1}:{2} {3}'.format(filename, e.lineNum, e.colNum, e.message)