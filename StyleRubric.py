from clang.cindex import Config, CursorKind, Index, TranslationUnitLoadError
import codecs
from cpplint import CleansedLines, RemoveMultiLineComments
from StyleError import StyleError
import sys

_CLANG_LIB_LOCATION = '/usr/local/Cellar/llvm/3.5.1/lib'


class StyleRubric(object):
    # Import helper functions
    from clangStyleHelpers import _cursorNotInFile, _findOperators, _operatorSpacingCheckHelper
    from clangStyleFunctions import evaluateOperatorSpacing

    def __init__(self):
        Config.set_library_path(_CLANG_LIB_LOCATION)
        # 'Global' state -- SHOULD NOT BE MODIFIED AFTER INIT
        self._clangIndex = Index.create()
        self._styleFunctions = self._loadFunctions()

        # Tracking for all files
        self._fileErrors = {}
        self._errorTypes = {}
        self._totalErrors = 0

        # Objects to maintain state of current file
        self._clangCursor = None
        self._currentFilename = None
        self._cleanLines = None
        pass

    # TODO: Take code from old rubric to load functions from modules
    def _loadFunctions(self):
        return

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
        self._clangCursor = None
        self._currentFilename = None
        self._cleanLines = None

    def _addError(self, label, line, column, data):
        self._totalErrors += 1
        if label not in self._errorTypes:
            self._errorTypes[label] = 0
        self._errorTypes[label] += 1
        self._fileErrors[self._currentFilename].append(StyleError(line, column, 0, label, data))

    def gradeFile(self, filename):
        self._resetForNextFile()
        assert self._clangCursor == None
        assert self._currentFilename == None
        assert self._cleanLines == None

        self._currentFilename = filename
        self._fileErrors[self._currentFilename] = []
        # parse will handle checking for appropriate file extensions
        try:
            self._clangCursor = self._clangIndex.parse(self._currentFilename).cursor
        except TranslationUnitLoadError:
            print 'Clang was unable to parse {}.'.format(filename)
            return

        data = self._safelyOpenFile()
        if data == None:
            return

        RemoveMultiLineComments(filename, data, '')
        self._cleanLines = CleansedLines(data)
        # Grade the file
        self.evaluateOperatorSpacing()