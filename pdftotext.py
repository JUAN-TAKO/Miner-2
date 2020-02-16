import shlex
import sys
import subprocess

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
    
file = sys.argv[1]
if not file.endswith(".pdf"):
    raise Exception("Le fichier doit être un pdf: " + file)

#check exists
pdf = open(file)
pdf.close()

escaped = shlex.quote(file)

text = subprocess.check_output('pdftotext -layout -enc UTF-8 ' + escaped + ' -', shell=True, encoding='utf-8')
text = str(text)
text = filter_text(text)
print(text)
if len(text) < 100:
    raise Exception('Le fichier est incorrect (trop petit): ' + file)