from miner import Miner
import glob, os
from multiprocessing.dummy import Pool as ThreadPool

def mine_pdf(args):
    (idx, m, file, is_pdf) = args
    try:
        if is_pdf:
            json = m.pdf_to_json(file, ['pdf_main', 'pdf_address'])
        else:
            f = open(file)
            text = f.read()
            f.close()
            json = m.text_to_json(text, ['dynaren_mail', 'dynaren_address'])
        print("[" + str(idx) + "] " + file + ": SUCCESS")
    except Exception as e:
        print("[" + str(idx) + "] " + file + ": FAILED")
        print(e)


pool = ThreadPool(4)

miner = Miner()

os.chdir("pdfs/dynaren")
i = 0
params = []
for file in glob.glob("*.txt"):
    i+=1
    params.append((i, miner, file, False))
    
pool.map(mine_pdf, params)
#print(json)