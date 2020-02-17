from lexer import Lexer
from rply import ParserGenerator
from ast import And, Or, Not, Assign, Rule, Weight
from ast import AssignList, Variable, Program
from ast import Number, Regex, Compare, Nop, BooleanCond
from ast import Conditional, Store, Force, Init

class Context():
    def __init__(self, text):
        self.text = text
        self.offset = 0
        self.active = {}
        self.output = {}
        self.variables = {}
        self.triggers = {}
        self.score = 0
        self.matches = 0
        self.changed = False

class Parser():
    def __init__(self, reg_refs):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            [rule.name for rule in Lexer().get_lexer().rules]
        )
        self.reg_refs = reg_refs
    
    def get_parser(self):
        return self.pg.build()

    def parse(self):
        @self.pg.production('program : rule SEMI_COLON program')
        def program(p):
            return Program(p[0], p[2])

        @self.pg.production('program : rule SEMI_COLON')
        def program_line(p):
            return p[0]
        
        @self.pg.production('rule : force')
        def force(p):
            return p[0]

        @self.pg.production('rule : once')
        def once(p):
            return p[0]

        @self.pg.production('rule : INIT assignements')
        def init(p):
            return Init(p[1])

        @self.pg.production('rule : start stop store')
        def rule(p):
            return Rule(p[0], p[1], p[2])

        @self.pg.production('once : ONCE delimitation or_condition set_vars')
        @self.pg.production('start : START delimitation or_condition set_vars')
        @self.pg.production('stop : STOP delimitation or_condition set_vars')
        def conditional(p):
            return Conditional(p[2], p[1], Weight(Number(0), p[3]))

        @self.pg.production('once : ONCE delimitation or_condition WEIGHT NBR set_vars')
        def once_weight(p):
            return Conditional(p[2], p[1], Weight(Number(p[4].getstr()), p[5]))

        @self.pg.production('force : FORCE STR TO STR')
        def force(p):
            return Force(p[3].getstr()[1:-1], p[1].getstr()[1:-1], BooleanCond(True))
        
        @self.pg.production('force : FORCE STR TO STR delimitation or_condition set_vars')
        def force_cond(p):
            cond = Conditional(p[5], p[4], Weight(Number(0), p[6]))
            return Force(p[3].getstr()[1:-1], p[1].getstr()[1:-1], cond)

        @self.pg.production('force : FORCE STR TO STR WEIGHT NBR delimitation or_condition set_vars')
        def force_cond_weight(p):
            cond = Conditional(p[7], p[6], Weight(Number(p[5].getstr()), p[8]))
            return Force(p[3].getstr()[1:-1], p[1].getstr()[1:-1], cond)

        @self.pg.production('store : STORE AS STR WEIGHT NBR')
        def store(p):
            return Store(p[2].getstr()[1:-1], Weight(Number(p[4].getstr()), Nop()))

        @self.pg.production('delimitation : WHEN')
        @self.pg.production('delimitation : AFTER')
        def delimitation(p):
            return p[0].gettokentype() == 'AFTER'
        
        @self.pg.production('or_condition : and_cond OR and_cond')
        def or_condition(p):
            return Or(p[0], p[2])
        
        @self.pg.production('or_condition : and_cond')
        def or_condition_nop(p):
            return p[0]
        
        @self.pg.production('and_cond : not_cond AND not_cond')
        def and_cond(p):
            return And(p[0], p[2])

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
            return Compare(Variable(p[0].getstr()), Number(p[2].getstr()))
        
        @self.pg.production('cond : REGEX')
        def regex(p):
            return Regex(p[0].getstr()[2:-2])
        
        @self.pg.production('cond : REG_REF')
        def reg_ref(p):
            return Regex(self.reg_refs[p[0].getstr()[1:]])
        
        @self.pg.production('set_vars : SET assignements')
        def set_vars(p):
            return p[1]
        
        @self.pg.production('set_vars :')
        def set_no_vars(p):
            return Nop()

        @self.pg.production('assignements : assign')
        def assignements_end(p):
            return AssignList(p[0], None)

        @self.pg.production('assignements : assign COMMA assignements')
        def assignements(p):
            return AssignList(p[0], p[2])

        @self.pg.production('assign : VAR EQUAL NBR')
        def assign(p):
            return Assign(Variable(p[0].getstr()), Number(p[2].getstr()))
        
    