from miner import Miner


miner = Miner()

json = miner.pdf_to_json('data/Fax_art_4.pdf', ['pdf_main', 'pdf_address'])

print(json)