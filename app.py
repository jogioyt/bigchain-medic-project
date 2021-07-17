from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from flask.helpers import flash, send_file
from pymongo import collection
from bdb_transaction import *
from rbac_methods import *
import pymongo
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5' 

#initiate bigchaindb
bdb_root_url = 'http://localhost:9984/'
bdb = BigchainDB(bdb_root_url)

#initiate namespace
namespace = "medical-app"

#get admin keys to create users
#get typeId to define the object of hospital, doctors, and patient

#Database for account
client = pymongo.MongoClient('localhost',27017)
db = client["medical_app"]

def signup(details_to_mongo, details_to_file):
	file_name = details_to_mongo["public_key"]+".txt"
	with open(file_name,'w') as file:
		file.write(json.dumps(details_to_file))
	file.close()

	#verify if the email already exist on the db
	if collection.find_one({"email":details_to_mongo['email']}):
		return jsonify({ "error": "Email address already in use" }), 400
	
	#send "user" list to database
	collection.insert_one(details_to_mongo)

	#insert the rbac's createUser transaction here
	flash("Account successfully created. Return to Login Page.")
	return send_file(file_name, as_attachment=True)

#Routes for Admin
@app.route('/dashboard')
def dashboard():
	return render_template("index_admin.html")

@app.route('/showAdminSignUpPage')
def showAdminSignUpPage():
	return render_template("admin_signup.html")

@app.route('/showAdminLoginPage')
def showAdminLoginPage():
	return render_template("admin_login.html")

@app.route('/admin_signUp')
def admin_signup():
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
		"public_key" : public_key,
		"role" : "admin"
	}
	
	#write user cred to a file.
	user_to_file = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key,
		"private_key" : private_key,
		"role" : "admin"
	}
	signup(user_to_mongo,user_to_file)
	session["role"] = "admin"
	session["name"] = set_name
	session["public_key"] = public_key
	return redirect(url_for('showHomePage'))
	"""
	file_name = public_key+".txt"
	with open(file_name,'w') as file:
		file.write(json.dumps(user_to_file))
	file.close()

	#verify if the email already exist on the db
	if db[].find_one({"email":user_to_mongo['email']}):
		return jsonify({ "error": "Email address already in use" }), 400
	
	#send "user" list to database
	collection.insert_one(user_to_mongo)

	#insert the rbac's createUser transaction here
	flash("Account successfully created. Return to Login Page.")
	return send_file(file_name, as_attachment=True)
	"""
#Routes for User
@app.route('/showUserLoginPage')
def showUserLoginPage():
	return render_template("user_login.html")

@app.route('/login', methods = ["POST"])
def login():
	get_email = request.form.get("email")
	get_password = request.form.get("password")
	login_cred = db["accounts"].find_one({"email":get_email})
	if login_cred:
		if login_cred['password'] == get_password:
			get_public_key = login_cred["public_key"]
			get_name = str(login_cred["name"])
			get_role = str(login_cred["role"])
			session["name"] = get_name
			session["public_key"] = get_public_key
			session["role"] = get_role
			print("Succesful. E-mail: "+str(get_email))
			return redirect(url_for('showHomePage'))
		else:
			return jsonify({ "error": "Login failed" }), 400

@app.route('/showUserSignUpPage')
def showUserSignUpPage():
	return render_template("user_signup.html")

@app.route('/user_signup', methods = ["POST"])
def user_signup():
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
		"public_key" : public_key,
		"role" : "doctor"
	}
	
	#write user cred to a file.
	user_to_file = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key,
		"private_key" : private_key,
		"role" : "doctor"
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

	#insert the rbac's createUser transaction here
	flash("Account successfully created. Return to Login Page.")
	return send_file(file_name, as_attachment=True)
 
#logout
@app.route('/logout')
def logout():
	if "public_key" in session:
		session.pop("public_key")
	return redirect(url_for('showUserLoginPage'))

#index page
@app.route('/')
def showHomePage():
	if "role" in session:
		if session["role"] == "doctor":
			welcome = "Hello! " + session["name"]
			return render_template("user_index.html", content = welcome)
		elif session["role"] == "admin":
			welcome = "Hello! " + session["name"]
			return render_template("admin_index.html", content = welcome)
	else:
		return redirect(url_for('showUserLoginPage'))

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
		birthplace = request.form.get("birthplace")
		birthday = request.form.get("birthday")
		ttl= birthplace + ", " + birthday
		alamat = request.form.get("alamat")
		sex = request.form.get("sex") #jenis kelamin
		gol_darah = request.form.get("gol_darah")
		
		#metadata
		#Anamnesis
		keluhan = request.form.get("keluhan")
		riwayat_penyakit_keluarga = request.form.get("riwayat_penyakit_keluarga")
		riwayat_penyakit_individu = request.form.get("riwayat_penyakit_individu")
		
		#Hasil Diagnosa
		hasil_fisik = request.form.get("hasil_fisik")
		hasil_organ = request.form.get("hasil_organ")
		hasil_kerja = request.form.get("hasil_kerja")

		#Rencana Penatalaksanaan Pasien
		rencana_kegiatan = request.form.get("rencana_kegiatan")
		rencana_waktu = request.form.get("rencana_waktu")
		rencana_hasil = request.form.get("rencana_hasil")
		rencana_comment = request.form.get("rencana_comment")
		
		#Hasil Penatalaksanaan pasien
		tanggal_treatment = request.form.get("tanggal_treatment")
		tindakan_treatment = request.form.get("tindakan_treatment")
		diagnosa_treatment = request.form.get("diagnosa_treatment")
		faktor_plus_treatment = request.form.get("faktor_plus_treatment")
		faktor_minus_treatment = request.form.get("faktor_minus_treatment")
		comment_treatment = request.form.get("comment_treatment")
		
		#Timestamp
		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

		#keypair
		private_key = request.form.get("private_key")
		public_key = session['public_key']

		#input asset dan metadata ke chain
		patient_asset = {
			'data' : {
				#rbac_shenanigans
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'jenis_kelamin' : sex,
					'alamat' : alamat,
					'gol_darah': gol_darah,
					'nama_dokter' : session["name"],
					'id_dokter' : session["id"]
				}
			}
		}
		metadata = {
			#can_link
			'timestamp':timestamp,
			'patient_meta': {
				'anamnesis':{
					'keluhan':keluhan,
					'riwayat_penyakit_keluarga':riwayat_penyakit_keluarga,
					'riwayat_penyakit_individu':riwayat_penyakit_individu
				},
				'hasil_diagnosa':{
					'hasil_fisik':hasil_fisik,
					'hasil_organ':hasil_organ,
					'hasil_kerja':hasil_kerja
				},
				'rencana':{
					'rencana_kegiatan':rencana_kegiatan,
					'rencana_waktu':rencana_waktu,
					'rencana_hasil':rencana_hasil,
					'rencana_comment':rencana_comment
				},
				'treatment':{
					'tanggal_treatment':tanggal_treatment,
					'tindakan_treatment':tindakan_treatment,
					'diagnosa_treatment':diagnosa_treatment,
					'faktor_plus_treatment':faktor_plus_treatment,
					'faktor_minus_treatment':faktor_minus_treatment,
					'comment_treatment' : comment_treatment
				}
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
		birthplace = request.form.get("birthplace")
		birthday = request.form.get("birthday")
		ttl= birthplace + ", " + birthday
		alamat = request.form.get("alamat")
		sex = request.form.get("sex") #jenis kelamin
		gol_darah = request.form.get("gol_darah")
		
		#metadata
		#Anamnesis
		keluhan = request.form.get("keluhan")
		riwayat_penyakit_keluarga = request.form.get("riwayat_penyakit_keluarga")
		riwayat_penyakit_individu = request.form.get("riwayat_penyakit_individu")
		
		#Hasil Diagnosa
		hasil_fisik = request.form.get("hasil_fisik")
		hasil_organ = request.form.get("hasil_organ")
		hasil_kerja = request.form.get("hasil_kerja")

		#Rencana Penatalaksanaan Pasien
		rencana_kegiatan = request.form.get("rencana_kegiatan")
		rencana_waktu = request.form.get("rencana_waktu")
		rencana_hasil = request.form.get("rencana_hasil")
		rencana_comment = request.form.get("rencana_comment")
		
		#Hasil Penatalaksanaan pasien
		tanggal_treatment = request.form.get("tanggal_treatment")
		tindakan_treatment = request.form.get("tindakan_treatment")
		diagnosa_treatment = request.form.get("diagnosa_treatment")
		faktor_plus_treatment = request.form.get("faktor_plus_treatment")
		faktor_minus_treatment = request.form.get("faktor_minus_treatment")
		comment_treatment = request.form.get("comment_treatment")
		
		#Timestamp
		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

		#keypair
		private_key = request.form.get("private_key")
		public_key = session['public_key']

		#input asset dan metadata ke chain
		tx_id = session["tx_id"]
		session.pop("tx_id")
		
		patient_asset = {
			'data' : {
				#rbac_shenanigans
				'patient' : {
					'nik_id' : nik_id,
					'nama' : nama,
					'ttl' : ttl,
					'jenis_kelamin' : sex,
					'alamat' : alamat,
					'gol_darah': gol_darah,
					'nama_dokter' : session["name"],
					'id_dokter' : session["id"]
				}
			}
		}
		metadata = {
			#can_link
			'timestamp':timestamp,
			'patient_meta': {
				'anamnesis':{
					'keluhan':keluhan,
					'riwayat_penyakit_keluarga':riwayat_penyakit_keluarga,
					'riwayat_penyakit_individu':riwayat_penyakit_individu
				},
				'hasil_diagnosa':{
					'hasil_fisik':hasil_fisik,
					'hasil_organ':hasil_organ,
					'hasil_kerja':hasil_kerja
				},
				'rencana':{
					'rencana_kegiatan':rencana_kegiatan,
					'rencana_waktu':rencana_waktu,
					'rencana_hasil':rencana_hasil,
					'rencana_comment':rencana_comment
				},
				'treatment':{
					'tanggal_treatment':tanggal_treatment,
					'tindakan_treatment':tindakan_treatment,
					'diagnosa_treatment':diagnosa_treatment,
					'faktor_plus_treatment':faktor_plus_treatment,
					'faktor_minus_treatment':faktor_minus_treatment,
					'comment_treatment' : comment_treatment
				}
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

