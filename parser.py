from lexer import Lexer
from rply import ParserGenerator
from ast import And, Or, Not, Assign
from ast import AssignList, Variable 
from ast import Number, Regex, Compare 
from ast import Delimitation, Source
from ast import Conditional, Store

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            [rule.name for rule in Lexer().get_lexer().rules]
        )
    
    def parse(self):
        @self.pg.production('program : rule SEMI_COLON program')
        def program(p):
            pass
        @self.pg.production('program : rule SEMI_COLON')
        def program_line(p):
            pass
        
        @self.pg.production('rule : force')
        @self.pg.production('rule : once')
        @self.pg.production('rule : start COMMA stop COMMA store')
        def rule(p):
            pass

        @self.pg.production('once : ONCE delimitation or_condition set_vars')
        @self.pg.production('start : START delimitation or_condition set_vars')
        @self.pg.production('stop : STOP delimitation or_condition set_vars')
        def conditional(p):
            return Conditional(p[2], p[3], p[1])

        @self.pg.production('force : STR AS STR IF condition set_vars')
        def force_cond(p):
            return Force(p[0].getstr(), p[1].getstr(), Conditional(p[4], p[5], Delimitation(False)))

        @self.pg.production('store : STORE AS STR WEIGHT NBR')
        def store(p):
            return Store(p[2].getstr(), Number(p[4]))
        
        @self.pg.production('source : HASH')
        @self.pg.production('source : STR')
        def source(p):
            return Source(p[0].gettokentype() == 'HASH')

        @self.pg.production('delimitation : WHEN')
        @self.pg.production('delimitation : AFTER')
        def delimitation(p):
            return Delimitation(p[0].gettokentype() == 'AFTER')
        
        @self.pg.production('or_condition : and_cond OR and_cond')
        def or_condition(p):
            return Or(p[0], p[2])
        
        @self.pg.production('or_condition : and_cond')
        def or_condition_nop(p):
            return p[0]
        
        @self.pg.production('and_cond : not_cond AND not_cond')
        def and_cond(p):
            return And(p[0], p[1])

        @self.pg.production('and_cond : not_cond')
        def and_cond_nop(p):
            return p[0]
        
        @self.pg.production('not_cond : NOT cond')
        def not_cond(p):
            return Not(p[1])

        @self.pg.production('not_cond : cond')
        def not_cond_nop(p):
            return p[0]

        @self.pg.production('cond : OPEN_PAREN or_condition CLOSE_PAREN')
        def paren(p):
            return p[1]
        
        @self.pg.production('cond : VAR EQUAL NBR')
        def equal(p):
            return Compare(Variable(p[0]), Number(p[2]))
        
        @self.pg.production('cond : REGEX')
        def regex(p):
            return Regex(p[0].getstr()[2:-2])
        
        @self.pg.production('set_vars : SET assignements')
        def set_vars(p):
            return p[1]
        
        @self.pg.production('assignements : assign')
        def assignements_end(p):
            return AssignList(p[1], None)

        @self.pg.production('assignements : assign COMMA assignements')
        def assignements(p):
            return AssignList(p[1], p[2])

        @self.pg.production('assign : VAR EQUAL NBR')
        def assign(p):
            return Assign(Variable(p[0].getstr()), Number(p[2].getstr()))
        
        