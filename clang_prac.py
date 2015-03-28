import codecs
import sys
import clang.cindex
from clang.cindex import CursorKind
from cpplint import CleansedLines


clang.cindex.Config.set_library_path('/usr/local/Cellar/llvm/3.5.1/lib')
index = clang.cindex.Index.create()

def safely_open(filename):
    try:
        dirty_text = codecs.open(filename, 'r', 'utf8', 'replace').readlines()
        for num, line in enumerate(dirty_text):
            dirty_text[num] = line.rstrip('\r')
        return dirty_text
    except IOError:
        sys.stderr.write('This file could not be read: "%s."  '
                         'Please check filename and resubmit \n' % filename)
        return


def find_operators(node, cursors, source_file):
    if (node.location.file and node.location.file.name != source_file):
        return
    if node.kind == CursorKind.BINARY_OPERATOR or \
        node.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR or \
        node.kind == CursorKind.UNARY_OPERATOR or \
        ((node.displayname == 'operator<<' or node.displayname == 'operator>>') and \
            node.kind == CursorKind.UNEXPOSED_EXPR):
        cursors.append(node)

    for n in node.get_children():
        find_operators(n, cursors, source_file)

def find_operator_start(code, start):
    index = start
    while index < len(code) and code[index] not in '+=-*/%!><&|':
        index += 1
    return index

def is_compound_binary(code, column):
    # if code[column] in '!=><&|':
    #     if code[column] in '!=<>' and column + 1 < len(code) and \
    #         code[column + 1] == '=':
    #         return True
    #     elif column + 1 < len(code) and code[column] == code[column + 1]:
    #         return True
    # return False
    return code[column:column + 2] in ['!=', '==', '<=', '>=', '&&', '||']

def evaluate_spacing(operator_cursors, clean_lines):
    lineNextStart = {}
    for c in operator_cursors:
        code = clean_lines.lines[c.location.line - 1]
        if c.location.line not in lineNextStart:
            lineNextStart[c.location.line] = c.location.column - 1
        index = find_operator_start(code, lineNextStart[c.location.line])
        lineNextStart[c.location.line] = index + 1
        # print 'Line: {} Index location: {} String slice: {}'.format(code[:-1], index,code[index:-1])
        if c.kind == CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
            lineNextStart[c.location.line] += 1
            if not is_spaced_correctly(code, index, True):
                print 'operator{0} is incorrectly spaced on line {1} column {2}'.format(code[index:index+2],
                                                                                        c.location.line,
                                                                                        index+1)
        elif c.kind == CursorKind.BINARY_OPERATOR:
            if is_compound_binary(code, index):
                lineNextStart[c.location.line] += 1
                if not is_spaced_correctly(code, index, True):
                 print 'operator{0} is incorrectly spaced on line {1} column {2}'.format(code[index:index+2],
                                                                                        c.location.line,
                                                                                        index+1)
            else:
                if not is_spaced_correctly(code, index, False):
                    print 'operator{0} is incorrectly space on line {1} column {2}'.format(code[index],
                                                                                       c.location.line,
                                                                                       index+1)
        elif c.kind == CursorKind.UNARY_OPERATOR:
            if index + 1 < len(code) and code[index] == code[index + 1]:
                lineNextStart[c.location.line] += 1
                print 'operator{} has no spacing rules, OKAY!'.format(code[index:index + 2])
            else:
                if index - 1 >= 0 and \
                    code[index - 1] not in [' ', '\n', '\r', '(']:
                    print 'operator{0} is incorrectly spaced on line {1} column {2}'.format(code[index],
                                                                                            c.location.line,
                                                                                            index+1)
        else: # operator>> and operator<<
            if not is_spaced_correctly(code, index, True):
                print '{0} is incorrectly spaced on line {1} column {2}'.format(c.displayname,
                                                                                c.location.line,
                                                                                index+1)

def is_spaced_correctly(code, column, is_compound):
    if column - 1 >= 0 and code[column - 1] not in [' ', '\n', '\r']:
        return False
    else:
        after_index = 2 if is_compound else 1
        if after_index + column < len(code) and code[column + after_index] not in [' ', '\n', '\r']:
            return False
    return True


def find_breaks(node, file_name, scope_stack):
    if node.location.file and node.location.file.name != file_name:
        return
    addedScope = False
    if node.kind == CursorKind.SWITCH_STMT:
        scope_stack.append('SWITCH')
        addedScope = True
    elif node.kind == CursorKind.FOR_STMT or \
            node.kind == CursorKind.WHILE_STMT or \
            node.kind == CursorKind.DO_STMT:
        scope_stack.append('LOOP')
        addedScope = True
    elif node.kind == CursorKind.BREAK_STMT:
        if len(scope_stack) == 0 or scope_stack[-1] != 'SWITCH':
            print 'You have an invalid use of break at line {0} column {1}'.format(node.location.line,
                                                                                   node.location.column)

    for n in node.get_children():
        find_breaks(n, file_name, scope_stack)
    if addedScope:
        scope_stack.pop()

def find_ternary(node, file_name):
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.CONDITIONAL_OPERATOR:
        print 'We advise against the use of the ternary operator in EECS 183 (line {} column {})'.format(node.location.line,
                                                                                                         node.location.column)
    for n in node.get_children():
        find_ternary(n, file_name)

def find_continues(node, file_name):
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.CONTINUE_STMT:
        print 'The use of continue is not allowed in EECS 183 (line {} column {})'.format(node.location.line,
                                                                                          node.location.column)
    for n in node.get_children():
        find_continues(n, file_name)

def find_gotos(node, file_name):
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.GOTO_STMT:
        print 'The use of goto is NOT allowed in eecs 183 (line {} column {})'.format(node.location.line,
                                                                                     node.location.column)
    for n in node.get_children():
        find_gotos(n, file_name)

def find_exit(node, file_name):
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.CALL_EXPR and node.displayname == 'exit':
        print 'stop'
    for n in node.get_children():
        find_exit(n, file_name)

def find_loop_children(node, file_name):
    '''
    TODO: WHILE_STMT child ordering: Conditional + Body
    TODO: DO_STMT child ordering: Do-body + Conditional
    TODO: Check conditional true/!false: CXX_BOOL_LITERAL_EXPR/UNARY_OPERATOR -> CXX_BOOL_LITERAL_EXPR child
    TODO: Check conditional 1/!0: IMPLICIT_CAST_EXPR -> INTEGER_LITERAL child/UNARY -> IMPLICIT + INTEGER
    '''
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.DO_STMT or node.kind == CursorKind.WHILE_STMT:
        loop_condition_cursor = None
        if node.kind == CursorKind.DO_STMT:
            loop_condition_cursor = [x for x in node.get_children()][1]
        else: # While_Stmt
            loop_condition_cursor = [x for x in node.get_children()][0]
        assert loop_condition_cursor

        if loop_condition_cursor.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
            print "Don't use while(true) line {} column {}".format(loop_condition_cursor.location.line,
                                                                    loop_condition_cursor.location.column)
        elif loop_condition_cursor.kind == CursorKind.UNARY_OPERATOR:
            # Find unary operator on the line, check if operator! and child is bool literal
            child = [x for x in loop_condition_cursor.get_children()][0]
            if child.kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
                print "Don't use while(!false) line {} column {}".format(loop_condition_cursor.location.line,
                                                                         loop_condition_cursor.location.column)

    for n in node.get_children():
        find_loop_children(n, file_name)

def find_bool_literal_comp(node, file_name, clean_lines):
    if node.location.file and node.location.file.name != file_name:
        return
    if node.kind == CursorKind.BINARY_OPERATOR:
        code = clean_lines.lines[node.location.line - 1]
        index = find_operator_start(code, node.location.column)
        if code[index:index+2] == '==' or code[index:index+2] == '!=':
            for child in node.get_children():
                if child.kind == CursorKind.UNEXPOSED_EXPR:
                    operands = [x for x in child.get_children()]
                    if operands[0].kind == CursorKind.CXX_BOOL_LITERAL_EXPR:
                        print 'Don\'t compare with true/false! line {} column {}'.format(node.location.line,
                                                                                   node.location.column)
                        break
    for n in node.get_children():
        find_bool_literal_comp(n, file_name, clean_lines)

full_suite = ['good.cpp', 'num_of_commands.cpp', 'test_valid_return.cpp', 'operator_spacing_bad.cpp',
                'operator_spacing_good.cpp', 'equals_true.cpp', 'goto_good.cpp', 'goto_bad.cpp',
                'break_bad.cpp', 'continue_good.cpp', 'continue_bad.cpp', 'ternary_good.cpp',
                'ternary_bad.cpp', 'while_true_good.cpp', 'while_true_bad.cpp', 'logical_AND_OR_spacing_bad.cpp',
                'logical_AND_OR_spacing_good.cpp', ]

individ_suite = ['operator_spacing_bad.cpp', 'operator_spacing_good.cpp']

def find_var_declaration(cursor, filename):
    if cursor.location.file and cursor.location.file.name != filename:
        return
    if cursor.kind == CursorKind.VAR_DECL:
        print 'stop'
    for n in cursor.get_children():
        find_var_declaration(n, filename)



for file_name in individ_suite:
    print 'Grading ' + file_name + '...'
    file_name = 'test/' + file_name
    data = safely_open(file_name)
    clean_lines = CleansedLines(data)
    try:
        tu = index.parse(file_name)
    except clang.cindex.TranslationUnitLoadError:
        print 'Failed to open test/{}. Moving to next file'.format(file_name)
        continue

    cursors = []
    find_operators(tu.cursor, cursors, file_name)
    evaluate_spacing(cursors, clean_lines)
    scope_stack = []
    find_breaks(tu.cursor, file_name, scope_stack)
    find_ternary(tu.cursor, file_name)
    find_continues(tu.cursor, file_name)
    find_exit(tu.cursor, file_name)
    find_gotos(tu.cursor, file_name)
    find_loop_children(tu.cursor, file_name)
    find_bool_literal_comp(tu.cursor, file_name, clean_lines)
    find_var_declaration(tu.cursor, file_name)
    for i in tu.get_includes():
        include_lib_name = i.location.file.name.split('/')[-1]
        if include_lib_name == 'sstream':
            print 'sstream included!'
    print '\n'