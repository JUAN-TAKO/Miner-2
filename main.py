from miner import Miner
import glob, os
from multiprocessing.dummy import Pool as ThreadPool

def mine_pdf(args):
    (idx, m, file) = args
    try:
        json = m.pdf_to_json(pdf, ['pdf_main', 'pdf_address'])
        print("[" + str(idx) + "] " + file + ": SUCCESS")
    except Exception as e:
        print("[" + str(idx) + "] " + file + ": FAILED")
        print(e)


pool = ThreadPool(4)

miner = Miner()

os.chdir("data")
i = 0
params = []
for pdf in glob.glob("*.pdf"):
    i+=1
    params.append((i, miner, pdf))
    
pool.map(mine_pdf, params)
#print(json)