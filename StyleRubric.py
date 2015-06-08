from clang.cindex import Config, CursorKind, Index, TranslationUnitLoadError
import clangStyleFunctions
import codecs
from ConfigParser import ConfigParser
from cpplint import CleansedLines, RemoveMultiLineComments
from StyleError import StyleError
import sys


_CLANG_LIB_LOCATION = '/usr/local/Cellar/llvm/3.5.1/lib'
_LINE_LENGTH_LIMIT = 90
_PROHIBITED_LIBRARIES = ['sstream']


class StyleRubric(object):
    # Import helper functions
    from clangStyleHelpers import _cursorNotInFile, _findOperators, _operatorSpacingCheckHelper
    SET_LIBRARY = True

    def __init__(self):
        # Prevent calling Config.set_library_path multiple times
        # which causes the rubric to crash
        self.config = ConfigParser()
        self.config.read('config.ini')
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

        self._maxLineLength = self.config.get('SETTINGS', 'line_length')
        self._prohibitedLibs = self.config.get('SETTINGS', 'prohibited_libraries').split(',')

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

    def _addError(self, label, line, column, data={}):
        self._totalErrors += 1
        if label not in self._errorTypes:
            self._errorTypes[label] = 0
        self._errorTypes[label] += 1
        self._fileErrors[self._currentFilename].append(StyleError(line, column, 0, label, data))

    def gradeFile(self, filename):
        self._resetForNextFile()
        assert self._translationUnit == None
        assert self._clangCursor == None
        assert self._currentFilename == None
        assert self._cleanLines == None

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
        if data == None:
            return

        RemoveMultiLineComments(filename, data, '')
        self._cleanLines = CleansedLines(data)
        # Grade the file
        for func in self._styleFunctions:
            func(self, self._clangCursor)