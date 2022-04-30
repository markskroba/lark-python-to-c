from lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL* statement_list

    statement_list: statement+ 

    ?statement: assignment | block

    ?block: (if_statement) _NL [_INDENT statement_list _DEDENT]

    assignment: var "=" expression _NL*

    if_statement: "if" expression ":"

    var: NAME

    ?expression: var
            | literal 
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

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """
test=1
test2=2
if test2==2:
    test3=3
    test4=4
    if test3==3:
        test4=4
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

    # if statements

    elif t.data == "block":
        x = translate(t.children[0])
        return x + "\n{\n" + '\n'.join(translate(t.children[1])) + "\n}"


    elif t.data == "if_statement":
        print(len(t.children))
        return f'if {translate(t.children[0])}:'

    elif t.data == "eq":
        print("TEST")
        lhs, rhs = t.children
        return f'{translate(lhs)} == {translate(rhs)}'
        

def test():
    parse_tree = parser.parse(test_tree)
    print("======CODE=======")
    print('\n'.join(translate(parse_tree)))
    print("======TREE=======")
    print(parse_tree.pretty())

if __name__ == '__main__':
    test()