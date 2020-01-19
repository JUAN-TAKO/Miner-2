from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('SET', r'set')
        self.lexer.add('INIT', r'init')
        self.lexer.add('AS', r'as')
        self.lexer.add('TO', r'to')
        self.lexer.add('WEIGHT', 'weight')
        #Lines
        self.lexer.add('ONCE', r'once')
        self.lexer.add('START', r'start')
        self.lexer.add('STOP', r'stop')
        self.lexer.add('STORE', r'store')
        self.lexer.add('FORCE', r'force')
        #Delimitations
        self.lexer.add('AFTER', r'after')
        self.lexer.add('WHEN', r'when')
        #Logic
        self.lexer.add('AND', r'and')
        self.lexer.add('OR', r'or')
        self.lexer.add('NOT', r'not')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        # Special
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('COMMA', r'\,')
        self.lexer.add('EQUAL', r'=')
        #Variable
        self.lexer.add('VAR', r'[a-zA-Z_][a-zA-Z0-9_]*')
        #Regex
        self.lexer.add('REGEX', r'\<\<.*\>\>')
        self.lexer.add('REG_REF', r'@[^\s]+')
        #String
        self.lexer.add('STR', r'\'[^\']*\'')
        #Number
        self.lexer.add('NBR', r'[0-9]+')
        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()