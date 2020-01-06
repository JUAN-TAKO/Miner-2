from lexer import Lexer
from mparser import Parser, Context

program = """
init a = 0;

once after <<\$>> set a = 1;

start when a = 1 set a = 2
stop after <<[0-9]{5}>>
store as 'result' weight 3;

force 'started' to 'true' when a = 2 set a = 3;
"""
text = """
ceci est un text de $test12345 fin.
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(program)

context = Context(text)

pg = Parser()
pg.parse()
parser = pg.get_parser()

tree = parser.parse(tokens)

for i in range(len(text)):
    context.offset = i
    tree.eval(context)

print(context.output)
print(context.variables)
print(context.active)