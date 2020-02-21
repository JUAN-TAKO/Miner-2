from lexer import Lexer
from mparser import Parser, Context
import rules
import sys
import fileinput 
import shlex
import subprocess
import json
import rply

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
        text = text.replace("\n", "$")
        text = text.replace("\r", "$")
        text = text.replace("\t", "$")
        text2 = ""

        while text2 != text:

            text2 = text
            text = text.replace("  ", "$")
            text = text.replace(" $", "$")
            text = text.replace("$ ", "$")
            text = text.replace("$$", "$")

        return text

    def mine(self, text, programsets):
        for programset_name in programsets:
            programset = rules.rules[programset_name]
            best_score = 0
            best_output = None
            for program in programset:
                tokens = self.lexer.lex(program["rules"])
                try:
                    ast = self.parser.parse(tokens)
                except Exception as e:
                    lpos = e.getsourcepos().lineno
                    cpos = e.getsourcepos().colno
                    line = program["rules"].splitlines()[lpos-1]
                    cursor = " " * cpos + "^"
                    raise Exception("Parsing error: " + str(e) + "\nat :\n\"" + line + "\"\n" + cursor)

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
    
    def filter_output(self, output):
        
        for k, v in output.items():
            t = v.replace("N° Police", "")
            t = t.strip("$")
            t = t.strip()
            t = t.replace("$", " ")

            output[k] = t

    def text_to_json(self, text, programsets):
        text = text = Miner.filter_text(str(text))

        if len(text) < 100:
            raise Exception('Le fichier est incorrect (trop petit): ' + file)
        
        print(text)
        data = self.mine(text, programsets)
        self.filter_output(data)

        return json.dumps(data)

    def pdf_to_json(self, file, programsets):
        if not file.endswith(".pdf"):
            raise Exception("Le fichier doit être un pdf: " + file)
        
        #check exists
        pdf = open(file)
        pdf.close()

        escaped = shlex.quote(file)

        text = subprocess.check_output('pdftotext -layout -enc UTF-8 ' + escaped + ' -', shell=True, encoding='utf-8')
        
        return self.text_to_json(text, programsets)
