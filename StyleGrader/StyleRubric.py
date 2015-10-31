from clang.cindex import Config, CursorKind, Index, TranslationUnitLoadError
import clangStyleFunctions
from clangStyleHelpers import isOperator
import codecs
from ConfigParser import ConfigParser
from cpplint import CleansedLines, RemoveMultiLineComments
import os.path
from StyleError import StyleError
import sys


class StyleRubric(object):
    # Import helper functions
    from clangStyleHelpers import _operatorSpacingCheckHelper
    SET_LIBRARY = True

    def __init__(self, optionalConfig=None):
        # Prevent calling Config.set_library_path multiple times
        # which causes the rubric to crash
        if (optionalConfig == None):
            self.config = ConfigParser()
            self.config.read('config.ini')
        else:
            self.config = optionalConfig
        if StyleRubric.SET_LIBRARY:
            Config.set_library_path(self.config.get('CLANG_LOCATION', 'path'))
            StyleRubric.SET_LIBRARY = False
        self.resetRubric()

    def resetRubric(self):
        # 'Global' state -- SHOULD NOT BE MODIFIED AFTER INIT
        self._clangIndex = Index.create()
        self._styleFunctions = self._loadFunctions()

        # Tracking for all files
        self._fileErrors = {}
        self._errorTypes = {}
        self._totalErrors = 0

        # Objects to maintain state of current file
        self._translationUnit = None
        self._clangCursor = None
        self._currentFilename = None
        self._cleanLines = None

        self._maxLineLength = int(self.config.get('SETTINGS', 'line_length'))
        self._prohibitedLibs = self.config.get('SETTINGS', 'prohibited_libraries').split(',')
        self._foundLibs = []
        self._stdLib = False

    def _loadFunctions(self):
        return clangStyleFunctions.__dir__()

    def _safelyOpenFile(self):
        try:
            dirty_text = codecs.open(self._currentFilename, 'r', 'utf8', 'replace').readlines()
            for num, line in enumerate(dirty_text):
                dirty_text[num] = line.rstrip('\r')
            return dirty_text
        except IOError:
            sys.stderr.write('This file could not be read: "%s."  '
                             'Please check filename and resubmit \n' % self._currentFilename)
            return None

    def _resetForNextFile(self):
        self._translationUnit = None
        self._clangCursor = None
        self._currentFilename = None
        self._cleanLines = None
        self._foundLibs = []
        self._stdLib = False

    def _addError(self, label, line, column, data={}):
        self._totalErrors += 1
        if label not in self._errorTypes:
            self._errorTypes[label] = 0
        self._errorTypes[label] += 1
        self._fileErrors[self._currentFilename].append(StyleError(line, column, 0, label, data))

    def _cursorNotInFile(self, cursor):
        '''
        Returns true if the provided cursor is in the rubric's
        current file, false otherwise
        :type cursor: clang.cindex.Cursor
        :return:
        '''
        return cursor.location.file and \
               cursor.location.file.name != self._currentFilename

    def _findOperators(self, cursor, operatorCursors):
        '''
        Collects any operator cursors encountered in the Clang AST
        and appends them to operatorCursors in a post-order traversal
        :type cursor: clang.cindex.Cursor
        :type operatorCursors: list[clang.cindex.Cursor]
        '''
        if self._cursorNotInFile(cursor):
            return
        # Treat AST traversal as post-order
        for c in cursor.get_children():
            self._findOperators(c, operatorCursors)
        if isOperator(cursor):
            operatorCursors.append(cursor)

    def getCode(self):
        '''
        Gets the entire list of the lines of code for the current file
        :return: list[str]
        '''
        return self._cleanLines.lines

    def getLineOfCode(self, lineNumber):
        '''
        Gets the line of code at lineNumber. If lineNumber is an invalid index,
        returns None
        :type lineNumber: int
        :return: str
        '''
        if lineNumber < 0 or lineNumber > len(self._cleanLines.lines):
            return None
        return self._cleanLines.lines[lineNumber]

    def gradeFile(self, filename):
        self._resetForNextFile()
        assert self._translationUnit is None
        assert self._clangCursor is None
        assert self._currentFilename is None
        assert self._cleanLines is None

        self._currentFilename = filename
        self._fileErrors[self._currentFilename] = []
        # parse will handle checking for appropriate file extensions
        try:
            self._translationUnit = self._clangIndex.parse(self._currentFilename)
            self._clangCursor = self._translationUnit.cursor
        except TranslationUnitLoadError:
            print 'Clang was unable to parse {}.'.format(filename)
            return

        data = self._safelyOpenFile()
        if data is None:
            return

        RemoveMultiLineComments(filename, data, '')
        self._cleanLines = CleansedLines(data)
        # Grade the file
        for func in self._styleFunctions:
            func(self, self._clangCursor)

        self._fileErrors[self._currentFilename].sort()

    def generateReport(self):
        report = {}
        for filename, errors in self._fileErrors.iteritems():
            # Use filenames as keys to the Report
            f = os.path.split(filename)[1]
            report[f] = []
            for e in errors:
                report[f].append('Line {}, Column {}: {}'.format(e.lineNum, e.colNum, e.message))
        return report

