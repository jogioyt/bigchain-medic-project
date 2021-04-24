"""
Pseudocode:
DEFINE class post
	SET payload
	SET bdb_ip
	SET public_key
	set private_key

	DEFINE function prepare(public key, payload)
	SET transactions = function prepare

	DEFINE function fulfill(transactions, private_key)
	DO function send_commit(fulfill)
"""

from flask import Flask
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

app = Flask(__name__)

@app.route('/')

def hello_world():
	return 'Hello World'

def prepare_transaction(payload, public_key):
	prepared_creation_tx = bdb.transactions.prepare(
    	operation = 'CREATE',
    	signers = public_key,
    	asset = payload,
	)
	return prepared_creation_tx

def fulfill(payload, private_key):
	fulfilled_creation_tx = bdb.transactions.fulfill(payload, private_key)
	return fulfilled_creation_tx

def main():
	bdb_root_url = 'http://34.101.231.183:9984/'
	
	bdb = BigchainDB(bdb_root_url)

	alice = generate_keypair()
	bob = generate_keypair()

	# contoh asset data untuk block
	 
	id_number = input("Masukkan nomor nomor id: ")
	patient_name = input("Masukkan nama pasien: ")
	symptoms = input("Masukkan gejala: ")
	division = input("Masukkan divisi RS: ")
	medication = input("Masukkan resep obat: ")
	comment = input("(Opsional) Masukkan Komentar: ")
	patient_data = {
		'data' : {
        	'patient' : {
            	'id_number' : id_number,
            	'patient_name': patient_name,
            	'symptoms' : symptoms,
            	'division' : division,
            	'medication' : medication
        	},
    	},
	}
	
	# contoh metadata untuk asset block
	metadata = {
		'comment' : comment
	}

	create_transaction(bdb,patient_data,metadata,alice)

if __name__== "__main__":
	main()


	
	
