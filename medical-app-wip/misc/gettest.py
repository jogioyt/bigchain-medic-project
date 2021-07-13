"""
Pseudocode:
DEFINE class get
	SET bdb_ip
	SET dbName
	set dataTopic
	set DATA[]

	if DataTopic "topic"
		DATA = Get from DB
	
	Return DATA
"""
from flask import Flask
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

app = Flask(__name__)

@app.route('/')

def hello_world():
	return 'Hello World'

def create_transaction(bdb, patient_data, metadata, user):
	pub_key = user.public_key
	priv_key = user.private_key
	prepared_creation_tx = bdb.transactions.prepare(
    	operation = 'CREATE',
    	signers = user.public_key,
    	asset = patient_data,
    	metadata = metadata,
	)
	fulfilled_tx = bdb.transactions.fulfill(prepared_creation_tx, priv_key)
	sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx)
	return sent_creation_tx

def retrieve(bdb, patientid):
	retrieved_tx = bdb.transactions.retrieve(patientid)
	return retrieved_tx

def append_transaction(bdb, tx, private_key):
	prep_transfer_transaction(bdb,)
	fulfilled_tx = bdb.transactions.fulfill(prepared_tx, private_keys)
	sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx) 


def burn_transaction(bdb, tx, private_keys):
	BURN_ADDRESS = "BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn"

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


	
	
