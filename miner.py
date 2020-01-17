from lexer import Lexer
from mparser import Parser, Context
import rules
import sys
import fileinput

class Miner():
    def __init__(self):
        self.lexer = Lexer().get_lexer()

        self.pg = Parser(rules.regexes)
        self.pg.parse()
        self.parser = self.pg.get_parser()

        self.final_output = {}

    @staticmethod
    def score(raw_score, nb_matches, min_score, max_score):
        total = 2 * raw_score - max_score
        accur = total / max_score
        fscore = accur * nb_matches
        if total >= min_score:
            return fscore

        return None

    @staticmethod
    def filter_text(text):
        text.replace("\n", "$")
        text.replace("\r", "$")
        text.replace("\t", "$")
        clean = False

        while not clean:
            text = text.replace("  ", "$")
            text = text.replace(" $", "$")
            text = text.replace("$ ", "$")
            text = text.replace("$$", "$")

            clean = clean or text.find("  ") != -1
            clean = clean or text.find(" $") != -1
            clean = clean or text.find("$ ") != -1
            clean = clean or text.find("$$") != -1

        return text

    def mine(self, text, programsets):
        text = Miner.filter_text(text)
        for programset_name in programsets:
            programset = rules.rules[programset_name]
            best_score = 0
            best_output = None
            for program in programset:
                tokens = self.lexer.lex(program["rules"])
                ast = self.parser.parse(tokens)
                context = Context(text)

                for i in range(len(text)):
                    context.offset = i
                    ast.eval(context)
                
                fscore = Miner.score(context.score, context.matches, program["min_score"], program["max_score"])
                if fscore is not None and fscore > best_score:
                    best_score = fscore
                    best_output = context.output
            
            if best_output is None:
                raise Exception("Impossible d'extraire les informations avec " + programset_name)

            self.final_output.update(best_output)
        
        return self.final_output
