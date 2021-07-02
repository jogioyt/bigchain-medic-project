from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from flask.helpers import flash, send_file
from pymongo import collection
from bdb_transaction import *
from functools import wraps
import pymongo
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5' 

#Database for account
client = pymongo.MongoClient('localhost',27017)
db = client["doctor"]
collection = db["users"]

#Routes
@app.route('/showLoginPage')

def showLoginPage():
	return render_template("login.html")

@app.route('/login', methods = ["POST"])
def login():
	get_email = request.form.get("email")
	get_password = request.form.get("password")
	login_cred = collection.find_one({"email":get_email})
	if login_cred:
		if login_cred['password'] == get_password:
			get_public_key = login_cred["public_key"]
			get_name = str(login_cred["name"])
			session["name"] = get_name
			session["public_key"] = get_public_key
			print("Succesful. E-mail: "+str(get_email))
			return redirect(url_for('showHomePage'))
		else:
			return jsonify({ "error": "Login failed" }), 400

@app.route('/showSignUpPage')

def showSignUpPage():
	return render_template("signup.html")

@app.route('/signup', methods = ["POST"])
def signup():
	#get credentials
	set_name = request.form.get("name")
	set_email = request.form.get("email")
	set_password = request.form.get("password")
	
	#generate keypair
	alice = generate_keypair()
	public_key = alice.public_key
	private_key = alice.private_key
	
	#compile keypair and credentials into a list named "user"
	user_to_mongo = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key
	}
	
	#write user cred to a file.
	user_to_file = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key,
		"private_key" : private_key
	}
	file_name = public_key+".txt"
	with open(file_name,'w') as file:
		file.write(json.dumps(user_to_file))
	file.close()

	#verify if the email already exist on the db
	if collection.find_one({"email":user_to_mongo['email']}):
		return jsonify({ "error": "Email address already in use" }), 400
	
	#send "user" list to database
	collection.insert_one(user_to_mongo)
	flash("Account successfully created. Return to Login Page.")
	return send_file(file_name, as_attachment=True)

#logout
@app.route('/logout')

def logout():
	if "public_key" in session:
		session.pop("public_key")
	return redirect(url_for('showLoginPage'))

#index page
@app.route('/')
def showHomePage():
	if "public_key" in session:
		welcome = "Hello! " + session["name"]
		return render_template("index.html", content = welcome)
	else:
		return redirect(url_for('showLoginPage'))

#route to create
@app.route("/create-form")

def showCreatePage():
	return render_template("create-form.html")

@app.route("/create-result", methods = ["POST","GET"])

def showCreateResult():
	if request.method == "POST":
		#Data untuk asset
		nik_id = request.form.get("nik_id")
		nama = request.form.get("nama")
		ttl = request.form.get("ttl")
		alamat = request.form.get("alamat")
		jk = request.form.get("jk")
		gol_darah = request.form.get("gol_darah")
		riwayat_penyakit_keluarga = request.form.get("riwayat_penyakit_keluarga")
		riwayat_penyakit_individu = request.form.get("riwayat_penyakit_individu")
		
		#metadata
		keluhan = request.form.get("gejala")
		hasil_inspeksi_fisik = request.form.get("hasil_inspeksi_fisik")
		hasil_diagnosa = request.form.get("hasil_diagnosa")
		administrasi = request.form.get("administrasi")
		data_perawatan = request.form.get("data_perawatan")
		comment = request.form.get("comment")
		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

		#keypair
		private_key = request.form.get("private_key")
		public_key = session['public_key']

		#input asset dan metadata ke chain
		patient_asset = {
			'data' : {
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'jenis_kelamin' : jk,
					'alamat' : alamat,
					'gol_darah': gol_darah,
					'riwayat_penyakit_keluarga' : riwayat_penyakit_keluarga,
					'riwayat_penyakit_individu' : riwayat_penyakit_individu,
					'nama_dokter' : session["name"],
					'id_dokter' : session["id"]
				}
			}
		}
		metadata = {
			'timestamp':timestamp,
			'patient_meta': {
				'keluhan' : keluhan,
				'hasil_inspeksi_fisik' : hasil_inspeksi_fisik,
				'hasi_diagnosa' : hasil_diagnosa,
				'administrasi' : administrasi,
				'data_perawatan' : data_perawatan,
				'comment' : comment
			}
		}
		user_keys = {
			'private_key' : private_key,
			'public_key' : public_key
		}
		tx = create_transaction(user_keys,patient_asset, metadata)
		print(tx)
		return render_template("create-result.html",content=tx)
	else:
		return redirect(url_for("showCreatePage "))
#route to search
@app.route("/search-form")

def showSearchPage():
	return render_template("search-form.html")

@app.route("/search-result", methods = ["POST","GET"])

def showSearchResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		print(tx)
		return render_template("search-result.html",content=tx)
	else:
		return redirect(url_for("showSearchPage"))

#route to append
@app.route("/search-append")

def showSearchAppendPage():
	return render_template("search-append.html")

@app.route("/append-form", methods = ["POST","GET"])
def showAppendForm():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		if(tx_id == tx['id']):
			return render_template("append-form.html",content=tx, tx_id = tx_id)
		else:
			return flash("The ID you insert is not valid.")
	else:
		return redirect(url_for("showSearchPage"))

@app.route("/append-result", methods = ["POST","GET"])
def showAppendResult():
	if request.method == "POST":
		#Data untuk asset
		nik_id = request.form.get("nik_id")
		nama = request.form.get("nama")
		ttl = request.form.get("ttl")
		alamat = request.form.get("alamat")
		jk = request.form.get("jk")
		gol_darah = request.form.get("gol_darah")
		riwayat_penyakit_keluarga = request.form.get("riwayat_penyakit_keluarga")
		riwayat_penyakit_individu = request.form.get("riwayat_penyakit_individu")
		
		#metadata
		keluhan = request.form.get("gejala")
		hasil_inspeksi_fisik = request.form.get("hasil_inspeksi_fisik")
		hasil_diagnosa = request.form.get("hasil_diagnosa")
		administrasi = request.form.get("administrasi")
		data_perawatan = request.form.get("data_perawatan")
		comment = request.form.get("comment")
		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

		#keypair
		private_key = request.form.get("private_key")
		public_key = session['public_key']

		#input asset dan metadata ke chain
		tx_id = session["tx_id"]
		session.pop("tx_id")
		patient_asset = {
			'id' : tx_id,
			'data' : {
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'jenis_kelamin' : jk,
					'alamat' : alamat,
					'gol_darah': gol_darah,
					'riwayat_penyakit_keluarga' : riwayat_penyakit_keluarga,
					'riwayat_penyakit_individu' : riwayat_penyakit_individu,
					'nama_dokter' : session["name"],
					'id_dokter' : session["id"]
				}
			}
		}
		metadata = {
			'timestamp':timestamp,
			'patient_meta': {
				'keluhan' : keluhan,
				'hasil_inspeksi_fisik' : hasil_inspeksi_fisik,
				'hasi_diagnosa' : hasil_diagnosa,
				'administrasi' : administrasi,
				'data_perawatan' : data_perawatan,
				'comment' : comment
			}
		}
		user_keys = {
			'private_key' : private_key,
			'public_key' : public_key
		}
		tx = append_transaction(tx_id,patient_asset,metadata,user_keys)
		return render_template("append-result.html",content=tx)
	else:
		return redirect(url_for("showSearchAppendPage"))

#route to burn

@app.route("/search-burn")

def showSearchBurnPage():
	return render_template("search-burn.html")

@app.route("/burn-result", methods = ["POST","GET"])

def showBurn():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		private_key = request.form.get("private_key")
		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
		metadata = {
			'timestamp':timestamp,
			'status':"burned"
		}		
		tx = burn_transaction(tx_id, metadata, private_key)
		print(tx)
		return render_template("burn-result.html",content=tx)
	else:
		return redirect(url_for("showSearchBurnPage"))

#route to transfer

@app.route("/search-transfer")

def showSearchTransferPage():
	return render_template("search-transfer.html")

@app.route("/transfer-result", methods = ["POST"])

def showTransferResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		address_id = request.form.get("address_id")
		private_key = request.form.get("private_key")
		public_key = session["public_key"]
		user_keys = {
			"public_key":public_key,
			"private_key":private_key
		}
		tf_tx = transfer_transaction(tx,user_keys,address_id)
		print(tf_tx)
		return render_template("transfer-result.html",content=tx)
	else:
		return redirect(url_for("showSearchTransferPage"))

if __name__== "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)

