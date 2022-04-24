from lark import Lark
from lark.indenter import Indenter

# tree_grammar = r"""
#     ?start: _NL* block

#     block: NAME | NAME _NL [_INDENT block+ _DEDENT]

#     %import common.CNAME -> NAME
#     %import common.WS_INLINE
#     %declare _INDENT _DEDENT
#     %ignore WS_INLINE

#     _NL: /(\r?\n[\t ]*)+/
# """

tree_grammar = r"""
    ?start: _NL* statement_list

    ?statement_list: statement+

    statement: NAME | block

    block: NAME _NL [_INDENT block+ _DEDENT]

    %import common.CNAME -> NAME
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
a
    b
    c
        d
        e
    f
        g
h
    i
j
k
"""

def test():
    print(parser.parse(test_tree).pretty())

if __name__ == '__main__':
    test()