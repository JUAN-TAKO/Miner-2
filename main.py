from miner import Miner


miner = Miner()

json = miner.pdf_to_json('data/fax_ser_8(31).pdf', ['pdf_main', 'pdf_address'])

print(json)