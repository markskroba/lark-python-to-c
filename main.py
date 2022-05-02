from lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL* statement_list

    statement_list: statement+ 

    ?statement: assignment | block

    ?block: (if_statement | else_statement | elif_statement) _NL [_INDENT statement_list _DEDENT]

    assignment: var "=" expression _NL*

    if_statement: "if" expression ":"
    else_statement: "else" ":"
    elif_statement: "elif" expression ":"

    var: NAME

    ?expression: var
            | literal 
            | "not" expression -> not
            | expression "or" expression -> or
            | expression "and" expression -> and
            | expression ">" expression -> gt
            | expression "<" expression -> lt
            | expression ">=" expression -> ge
            | expression "<=" expression -> le
            | expression "==" expression -> eq

    literal: NUMBER

    %import common.CNAME -> NAME
    %import common.INT -> NUMBER 
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE

    _NL: /(\r?\n[\t ]*)+/
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

parser = Lark(tree_grammar, parser='earley', postlex=TreeIndenter())

test_tree = """
if test2==2:
    test1=2
elif test3==3:
    test2=2
else:
    test3=3
"""

def translate(t):
    if t.data == "statement_list":
        x = map(translate, t.children)
        return [a for a in map(translate, t.children)]
    elif t.data == "assignment":
        lhs, rhs = t.children
        return f'int {translate(lhs)} = {translate(rhs)};'
    elif t.data in ["literal", "var"]:
        return t.children[0]

    # parsing blocks
    elif t.data == "block":
        x = translate(t.children[0])
        return x + "\n{\n" + '\n'.join(translate(t.children[1])) + "\n}"
    elif t.data == "if_statement":
        return f'if ({translate(t.children[0])})'

    # parsing expressions
    elif t.data == "or":
        lhs, rhs = t.children
        return(f'{translate(lhs)} || {translate(rhs)}')
    elif t.data == "and":
        lhs, rhs = t.children
        return(f'{translate(lhs)} && {translate(rhs)}')
    elif t.data == "not":
        # not working rn, needs fix
        lhs = t.children
        return(f'!{translate(lhs)}')
    elif t.data == "eq":
        lhs, rhs = t.children
        return f'{translate(lhs)} == {translate(rhs)}'
    elif t.data == "gt":
        lhs, rhs = t.children
        return f'{translate(lhs)} > {translate(rhs)}'
    elif t.data == "lt":
        lhs, rhs = t.children
        return f'{translate(lhs)} < {translate(rhs)}'
    elif t.data == "ge":
        lhs, rhs = t.children
        return f'{translate(lhs)} >= {translate(rhs)}'
    elif t.data == "le":
        lhs, rhs = t.children
        return f'{translate(lhs)} <= {translate(rhs)}'

        


def test():
    parse_tree = parser.parse(test_tree)
    print("======CODE=======")
    # print('\n'.join(translate(parse_tree)))
    print("======TREE=======")
    print(parse_tree.pretty())

if __name__ == '__main__':
    test()