from lark import Lark
from lark.indenter import Indenter

# tree_grammar = r"""
#     ?start: _NL* statement_list

#     ?statement_list: statement+

#     statement: NAME | block

#     block: NAME _NL [_INDENT block+ _DEDENT]

#     %import common.CNAME -> NAME
#     %import common.WS_INLINE
#     %declare _INDENT _DEDENT
#     %ignore WS_INLINE

#     _NL: /(\r?\n[\t ]*)+/
# """
tree_grammar = r"""
    ?start: _NL* statement_list

    statement_list: statement+ 

    statement: (assignment | block) 


    block: (if_statement) _NL [_INDENT statement+ _DEDENT]

    assignment: var "=" expression _NL*

    if_statement: "if" expression ":"

    var: NAME

    expression: var
            | NUMBER 
            | expression ">" expression -> gt
            | expression "<" expression -> lt
            | expression ">=" expression -> ge
            | expression "<=" expression -> le
            | expression "==" expression -> eq

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
test=2
if test==1:
    test2 = 2
    if test==1:
        test3=3
    test1 = 1
test=1
"""

def test():
    print(parser.parse(test_tree).pretty())

if __name__ == '__main__':
    test()