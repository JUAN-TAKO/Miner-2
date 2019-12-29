from lexer import Lexer

text_input = """
start when a = 1 set a = 2,
stop after <<[0-9]{5}>>,
store # as 'result';
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

for token in tokens:
    print(token)