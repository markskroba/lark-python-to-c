from lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL* statement_list

    statement_list: statement+ 

    ?statement: assignment | block | return_statement

    ?block: (if_statement | else_statement | elif_statement | function_signature) _NL [_INDENT statement_list _DEDENT]

    assignment: var "=" expression _NL*
    return_statement: "return" expression _NL*

    if_statement: "if" expression ":"
    else_statement: "else" ":"
    elif_statement: "elif" expression ":"

    function: var "(" parameters ")"
    function_signature: "def" function ":"
    parameters: (var ",")* var*

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

            | expression binary_operator expression -> binary

    

    literal: NUMBER
    ?binary_operator: "*" -> binary_multiply
                | "/" -> binary_divide
                | "%" -> binary_remainder
                | "+" -> binary_add
                | "-" -> binary_substract

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
def fact(n, m, j, k):
    i = 0
    r = 0
    r = 1
    r = r + 1

    return r
"""

fact = """
def fact(n):
    i = 0
    r = 0
    r = 1
    r = 2 + 2
    for i in range(2, n+1):
        print(i)
    
    return r

if __name__ == "__main__":
    print(fact(10))
"""

def translate(t):
    if t.data == "statement_list":
        x = map(translate, t.children)
        return [a for a in map(translate, t.children)]

    elif t.data == "assignment":
        lhs, rhs = t.children

        if translate(rhs) == "0":
            return f'int {translate(lhs)};'
        else:
            return f'{translate(lhs)} = {translate(rhs)};'
    elif t.data == "return_statement":
        return f'return {translate(t.children[0])};'
    elif t.data in ["literal", "var"]:
        return t.children[0]

    # parsing blocks
    elif t.data == "block":
        x = translate(t.children[0])
        return x + "\n{\n" + '\n'.join(translate(t.children[1])) + "\n}"
    elif t.data == "if_statement":
        return f'if ({translate(t.children[0])})'
    elif t.data == "elif_statement":
        return f'else if ({translate(t.children[0])})'
    elif t.data == "else_statement":
        return 'else'

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

    # functions
    elif t.data == "function":
        func_name, func_parameters = t.children

        return f'{translate(func_name)}({translate(func_parameters)})'
    elif t.data == "function_signature":
        func = t.children[0]

        return translate(func)
    elif t.data == "parameters":
        return ", ".join(map(translate, t.children))


    # translating binary operations
    elif t.data == "binary":
        lhs, operator, rhs = t.children
        return f'{translate(lhs)} {translate(operator)} {translate(rhs)}'
    elif t.data == "binary_multiply":
        return "*"
    elif t.data == "binary_divide":
        return "/"
    elif t.data == "binary_remainder":
        return "%"
    elif t.data == "binary_add":
        return "+"
    elif t.data == "binary_substract":
        return "-"


def test():
    parse_tree = parser.parse(test_tree)
    print("======TREE=======")
    print(parse_tree.pretty())
    print("======CODE=======")
    print('\n'.join(translate(parse_tree)))
    # test_translate(parse_tree)

if __name__ == '__main__':
    test()