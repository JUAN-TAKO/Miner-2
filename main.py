from miner import Miner
import glob, os
from multiprocessing.dummy import Pool as ThreadPool

def mine_pdf(args):
    (idx, m, file, is_pdf) = args
    try:
        if is_pdf:
            json = m.pdf_to_json(file, ['homeserve'])
        else:
            f = open(file)
            text = f.read()
            f.close()
            #print(text)
            json = m.text_to_json(text, ['dynaren_main', 'dynaren_address'])
        print("\n\n[" + str(idx) + "] " + file + ": SUCCESS\n")
        print(json)
    except Exception as e:
        print("[" + str(idx) + "] " + file + ": FAILED\n")
        print(e)


pool = ThreadPool(1)

miner = Miner()

os.chdir("pdfs/hsvm")
i = 0
params = []
for file in glob.glob("*.pdf"):
    i+=1
    params.append((i, miner, file, True))
    
pool.map(mine_pdf, params)
#print(json)