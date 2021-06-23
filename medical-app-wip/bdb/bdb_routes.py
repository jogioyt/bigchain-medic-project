from flask import flask, request, session, render_template, redirect, url_for
from app import app
from bdb_transaction import *
from datetime import datetime

#BigchainDB init
bdb_root_url = 'http://34.101.177.101:9984/'
bdb = BigchainDB(bdb_root_url)

#create transaction
@app.route("/create", methods = ["POST"])
def create():
	if request.method == "POST":
		nik_id = request.form.get("nik_id")
		nama = request.form.get("nama")
		ttl = request.form.get("ttl")
		alamat = request.form.get("alamat")
		gejala = request.form.get("gejala")
		comment = request.form.get("comment")
		private_key = request.form.get("private_key")
		public_key = session['public_key']
		#insert the asset which consists 
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
		user_keys = {
			'private_key' : private_key,
			'public_key' : public_key
		}
		sent_creation_tx = create_medical_data(patient_asset,user_keys)
		return render_template("create-result.html",content=sent_creation_tx)
	else:
		return redirect(url_for("showCreatePage "))

#retrieve transaction
@app.route("/retrieve", methods = ["POST"])

def retrieve():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_medical_data(tx_id)
		print(tx)
		return render_template("search-result.html",content=tx)
	else:
		return redirect(url_for("showSearchPage"))

@app.route("/append", methods = ["POST"])
def append():
	if request.method == "POST":
		nik_id = request.form.get('nik_id')
		nama = request.form.get('nama')
		ttl = request.form.get('ttl')
		alamat = request.form.get('alamat')
		gejala = request.form.get('gejala')
		comment = request.form.get("comment")
		tx_id = request.form.get('tx_id')
		patient_asset = {
			'id': tx_id
		}
        private_key = request.form.get("private_key")
        public_key = session['public_key']
        user_keys = {
			'private_key' : private_key,
			'public_key' : public_key
		}
        tx = update_medical_data(tx_id,patient_asset,user_keys)
        return render_template("append-result.html",content=tx)

@app.route("/burn", methods = ["POST","GET"])
def burn():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		private_key = request.form.get("private_key")
		tx = delete_medical_data(tx_id,private_key)
		print(tx)
		return render_template("burn-result.html",content=tx)
	else:
		return redirect(url_for("showSearchBurnPage"))

@app.route("/transfer", methods = ["POST"])
def transfer():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		address_id = request.form.get("address_id")
		private_key = request.form.get("private_key")
		tx = transfer_medical_data(tx_id,private_key,address_id)
		print(tx)
		return render_template("transfer-result.html",content=tx)
	else:
		return redirect(url_for("showSearchTransferPage"))
