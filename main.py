from lark import Lark
from lark.indenter import Indenter
import sys

tree_grammar = r"""
    ?start: _NL* statement_list

    statement_list: statement+ 

    ?statement: (assignment | block | return_statement | break_statement | print_function | expression | range_function) _NL*

    ?block: (if_statement | else_statement | elif_statement | function_signature | while_statement | for_statement) _NL [_INDENT statement_list _DEDENT]

    assignment: var "=" expression
    return_statement: "return" expression
    break_statement: "break"

    if_statement: "if" expression ":"
    else_statement: "else" ":"
    elif_statement: "elif" expression ":"

    while_statement: "while" expression ":"
    for_statement: "for" var "in" range_function ":"

    function: var "(" parameters ")"
    function_signature: "def" function ":"
    parameters: (expression ",")* expression*

    print_function: "print" "(" string ")" -> print_string
                    | "print" "(" string ".format(" ((expression) ","*)* ")"* -> print_format
    range_function: "range" "(" literal ("," (literal|"-"literal))~0..2 ")"

    var: NAME
    string: STRING

    ?expression: var
            | literal
            | string
            
            | function
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
    %import common.ESCAPED_STRING -> STRING
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
i = 0
j = 0
print("j={}".format(j))
print("test print")

while i == 0 and j == 0:
    print("{}".format(i))
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

fib = """
def fib(n):
    if n <= 2:
        return 1
    else: 
        return fib(n-1) + fib(n-2)

print("{}".format( "test", fib(1,2)))
if __name__ == "__main__":
    print("test")

    for i in range(10,1,-1):
        print("test")
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
    elif t.data == "break_statement":
        return "brake;"
    elif t.data in ["literal", "var", "string"]:
        return t.children[0]

    elif t.data == "block":
        x = translate(t.children[0])
        return x + "\n{\n" + '\n'.join(translate(t.children[1])) + "\n}"
    elif t.data == "if_statement":

        condition = translate(t.children[0])
        if condition == "__name__ == \"__main__\"":
            return f'int main()'

        return f'if ({condition})'
    elif t.data == "elif_statement":
        return f'else if ({translate(t.children[0])})'
    elif t.data == "else_statement":
        return 'else'
    
    elif t.data == "while_statement":
        return f'while ({translate(t.children[0])})'
    elif t.data == "for_statement":
        conditions = translate(t.children[1])
        variable = translate(t.children[0])
        print(int(conditions[2]))
# 
        if len(conditions) == 1:
            start = 0
            stop = conditions[0]
            step = 1
        elif len(conditions) == 2:
            start = conditions[0]
            stop = conditions[1]
            step = 1
        elif len(conditions) == 3:
            start = conditions[0]
            stop = conditions[1]
            step = conditions[2]
                
        if start > stop:
            return f'for (int {variable} = {start}; {variable} > {stop}; {variable} -= {step})'
        else:
            return f'for (int {variable} = {start}; {variable} < {stop}; {variable} += {step})'
    elif t.data == "range_function":
        return [x for x in map(translate, t.children)]

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
    
    elif t.data == "print_string":
        return f'printf({translate(t.children[0])});'
    elif t.data == "print_format":
        return f'printf({(translate(t.children[0]).replace("{}", "%i"))}, {", ".join(map(translate, t.children[1:]))});'

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
    parse_tree = parser.parse(fib)
    print("======TREE=======")
    print(parse_tree.pretty())
    print("======CODE=======")
    print('#include <stdio.h>\n' + '<>\n'.join(translate(parse_tree)))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Pass the path to the file you want to translate as argument")
    else:
        with open(sys.argv[1], "r") as f:
            parse_tree = parser.parse(f.read())
            print(parse_tree.pretty())
            print('#include <stdio.h>\n' + '<>\n'.join(translate(parse_tree)))
