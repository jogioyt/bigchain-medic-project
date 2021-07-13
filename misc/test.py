from flask import Flask, render_template, request, redirect, url_for
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from bdb_transaction import *

app = Flask(__name__)

#halaman index
@app.route('/')

def showHomePage():
	return render_template("index.html")

#menuju create
@app.route("/create-form", methods = ["POST","GET"])

def showCreatePage():
	return render_template("create-form.html")

@app.route("/create-result", methods = ["POST","GET"])

def showCreateResult():
	if request.method == "POST":
		nik_id = request.form["nik_id"],
		nama = request.form["nama"],
		ttl = request.form["ttl"],
		alamat = request.form["alamat"],
		gejala = request.form["gejala"],
		comment = request.form["comment"]
		patient_asset = {
			'data' : {
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'alamat' : alamat,
					'gejala' : gejala,
					'comment' : comment
				}
			}
		}
		bdb_root_url = 'http://34.101.231.183:9984/'
		bdb = BigchainDB(bdb_root_url)
		tx = create_medical_data(bdb,patient_asset)
		return render_template("create-result.html",content=tx)
	else:
		return redirect(url_for("showCreatePage "))

#menuju search
@app.route("/search-form", methods = ["POST","GET"])

def showSearchPage():
	return render_template("search-form.html")

@app.route("/search-result", methods = ["POST","GET"])

def showSearchResult():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		bdb_root_url = 'http://34.101.231.183:9984/'
		bdb = BigchainDB(bdb_root_url)
		tx = retrieve_medical_data(bdb,tx_id)
		return render_template("search-result.html",content=tx)
	else:
		return redirect(url_for("showSearchPage"))

#menuju append
@app.route("/search-form", methods = ["POST","GET"])

def showSearchAppendPage():
	return render_template("search-append.html")

@app.route("/append-form", methods = ["POST","GET"])
def showAppendForm():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		bdb_root_url = 'http://34.101.231.183:9984/'
		bdb = BigchainDB(bdb_root_url)
		tx = retrieve_medical_data(bdb,tx_id)
		return render_template("append-form.html",content=tx, tx_id = tx_id)
	else:
		return redirect(url_for("showSearchPage"))

@app.route("/append-result", methods = ["POST","GET"])
def showAppendResult():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		nik_id = request.form["nik_id"],
		nama = request.form["nama"],
		ttl = request.form["ttl"],
		alamat = request.form["alamat"],
		gejala = request.form["gejala"],
		comment = request.form["comment"]
		patient_asset = {
			'data' : {
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'alamat' : alamat,
					'gejala' : gejala,
					'comment' : comment
				}
			}
		}
		bdb_root_url = 'http://34.101.231.183:9984/'
		bdb = BigchainDB(bdb_root_url)
		tx = transfer_medical_data(bdb, tx_id,patient_asset)
		return render_template("append-result.html",content=tx)
	else:
		return redirect(url_for("showSearchPage"))

"""
def append_transaction(bdb, tx, private_key):
	prep_transfer_transaction(bdb,)
	fulfilled_tx = bdb.transactions.fulfill(prepared_tx, private_keys)
	sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx)
"""

#menuju burn
"""
@app.route("/burn")

def burn_transaction(bdb, tx, private_keys):
	BURN_ADDRESS = "BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn"
    transfer_asset = {
		'id': get_transaction_id
    } 
	output = get_tx['outputs'][0]
    transfer_input = {
		'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':get_transaction_id,
        },
        'owners_before': output['public_keys'],
    }
    prepared_burn_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        asset = transfer_asset,
        inputs = transfer_input,
        recipients= BURN_ADDRESS,
	)
    fulfillBurnTransaction = bdb.transactions.fulfill(
        prepared_burn_tx, 
        private_keys,
    )
    signed_burn_tx = bdb.transactions.send_commit(fulfillBurnTransaction)

"""

if __name__== "__main__":
	app.run(debug=True)