from lark import Lark

my_grammar = """
?start: statement_list

statement_list: statement+

?statement: assignment 
            | if_statement
            | puts_statement
            | while_statement
            | unless_statement

assignment: var "=" expression

var: NAME

if_statement: "if" expression statement_list "end"
unless_statement: "unless" expression statement_list "end"
while_statement: "while" expression "do" statement_list "end"
puts_statement: "puts" expression

?expression: var
            | literal
            | expression ">" expression -> gt
            | expression "<" expression -> lt
            | expression ">=" expression -> ge
            | expression "<=" expression -> le
            | expression "==" expression -> eq

literal: NUMBER

%import common.CNAME -> NAME
%import common.WS
%import common.INT -> NUMBER 
%ignore WS
"""

def translate(t):

  if t.data == 'statement_list':
    return '\n'.join(map(translate, t.children))
  elif t.data == 'if_statement':
    condition, block = t.children
    return 'if' + ' (' + translate(condition) + ') {\n'+ translate(block) + '\n}\n'
  elif t.data == 'puts_statement':
    exp = t.children[0]
    return 'print ' + translate(exp) + '."\\n";'
  elif t.data == 'var':
    return '$'+t.children[0]
  elif t.data == 'literal':
    return t.children[0]
  elif t.data == 'gt':
    lhs, rhs = t.children
    return translate(lhs) + ' > ' + translate(rhs)
  elif t.data == 'assignment':
    lhs, rhs = t.children
    return translate(lhs) + ' = ' + translate(rhs) + ';'
  else:
    raise SyntaxError("bad tree")


parser = Lark(my_grammar)
program = """
x = 5
y = 8
c = 0
if y>x
  c = 4
end
puts c
"""
parse_tree = parser.parse(program)
print(translate(parse_tree))
#print(parse_tree.pretty())
