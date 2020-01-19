from lexer import Lexer
from mparser import Parser, Context
import rules
program = """
init a = 0, r = 0;

once after <<\$>> set a = 1;

start when r=0 and <<[0-9]{5}>>
stop after <<[0-9]{5}>> set r=1
store as 'Ref' weight 1;

force 'started' to 'true' when a = 2 set a = 3;

start after <<\$>>
stop when <<5>>
store as '!' weight 1;
"""
text = """
ceci !est! un text de $test12345 fin.
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(program)

context = Context(text)

pg = Parser(rules.regexes)
pg.parse()
parser = pg.get_parser()

tree = parser.parse(tokens)

for i in range(len(text)):
    context.offset = i
    tree.eval(context)

print(context.output)
print(context.variables)
print(context.active)