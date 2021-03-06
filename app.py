#Dependecies
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from flask.helpers import flash, send_file
import pymongo
import json
import os
from datetime import datetime

#Homemade Modules
from bdb_transaction import *
from rbac_methods import *
from setup import *
from decentralization_test import createTest

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5' 

#rbac stuff
#initiate namespace
namespace = "medical-app"
#admin type
admin_type = getAdminType()
admin_type_id = admin_type["id"]

#app details
app_tx = getApp()
app_tx_id = admin_type["id"]

#get typeId to define the object of hospital, ... 
hospital_type = getHospitalType()
hospital_type_id = hospital_type["id"]

# ...doctors, ... 
doctor_type = getDoctorType()
doctor_type_id = doctor_type["id"]

# ...and patient
patient_type = getPatientType()
patient_type_id = patient_type["id"]

#Database for account
client = pymongo.MongoClient('localhost',27017)
db = client["medical_app"]

#Routes for Admin
@app.route('/dashboard')
def dashboard():
	return render_template("admin_index.html")

@app.route('/AdminSignUpPage')
def AdminSignUpPage():
	return render_template("admin_signup.html")

@app.route('/AdminLoginPage')
def AdminLoginPage():
	return render_template("admin_login.html")

@app.route('/admin_login', methods = ["POST"])
def admin_login():
	get_email = request.form.get("email")
	get_password = request.form.get("password")
	login_cred = db["admin_accounts"].find_one({"email":get_email})
	if login_cred:
		if login_cred['password'] == get_password:
			get_public_key = login_cred["public_key"]
			get_name = str(login_cred["name"])
			get_role = str(login_cred["role"])
			session["name"] = get_name
			session["public_key"] = get_public_key
			session["role"] = get_role
			print("Succesful. E-mail: "+str(get_email))
			return redirect(url_for('dashboard'))
		else:
			return jsonify({ "error": "Login failed" }), 400

@app.route('/admin_signup', methods = ["POST"])
def admin_signup():
	#get credentials
	set_name = request.form.get("name")
	set_email = request.form.get("email")
	set_password = request.form.get("password")
	
	#verify if the email already exist on the db
	if db["admin_accounts"].find_one({"email":set_email}):
		return jsonify({ "error": "Email address already in use" }), 400

	#generate keypair
	bob = generate_keypair()
	public_key = bob.public_key
	private_key = bob.private_key
	bob_keypairs = {
		'public_key': public_key,
		'private_key': private_key
	}
	
	#compile keypair and credentials into a list named "user"
	user_to_mongo = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key,
		"role" : "admin"
	}

	#apply rbac createUser and createTypeInstance
	admin_user_rbac = createUser(namespace, bob_keypairs, admin_type_id, 'admin', public_key, user_to_mongo)

	admin_user_rbac_id = admin_user_rbac["id"]

	rbac = {
		"user_rbac_id": admin_user_rbac_id
	}

	print(admin_user_rbac)

	#add the rbac to mongo dict
	user_to_mongo.update(rbac)
	
	#send "user" list to database
	db["admin_accounts"].insert_one(user_to_mongo)

	#write user cred to a file.
	user_to_file = {
		"name" : set_name,
		"email" : set_email,
		"password" : set_password,
		"public_key" : public_key,
		"private_key" : private_key,
		"role" : "admin",
		"user_rbac_id": admin_user_rbac_id
	}

	#set session
	session["role"] = "admin"
	session["name"] = set_name
	session["public_key"] = public_key
	
	#send file
	file_name = set_name+"_admin_"+public_key+".txt"
	completedFilename = os.path.join(os.path.expanduser('~'),"medical-app/application/admin_account",file_name)
	with open(completedFilename,'w') as file:
		file.write(json.dumps(user_to_file))
	file.close()

	#insert the rbac's createUser transaction here
	flash("Account successfully created. Return to Login Page.")
	return send_file(completedFilename, as_attachment=True)

#UNDER CONSTRUCTION

@app.route('/AddHospitalPage')
def AddHospitalPage():
	return render_template("admin-create-hospital-form.html", key = session["public_key"])

@app.route('/add_hospital', methods = ["POST"])
def add_hospital():
	#get credentials
	set_name = request.form.get("rs_nama")
	set_address_street = request.form.get("rs_alamat_jalan")
	set_address_city = request.form.get("rs_alamat_kota")
	set_address_province = request.form.get("rs_alamat_provinsi")
	set_tendermint_address = request.form.get("tendermint_address")
	set_tendermint_pub_key = request.form.get("tendermint_public_key")
	set_tendermint_node_id = request.form.get("tendermint_node_id")

	#generate keypair
	private_key = request.form.get("private_key")
	public_key = request.form.get("public_key")

	admin_keys = {
		'private_key':private_key,
		'public_key':public_key
	}
	
	set_address = str(set_address_street)+", "+str(set_address_city)+", "+str(set_address_province)

	#compile keypair and credentials into a list named "user"
	user_to_mongo = {
		"name" : set_name,
		"address" : set_address,
		"role" : "hospital",
		"tendermint":{
			"t_address":set_tendermint_address,
			"t_pub_key":set_tendermint_pub_key,
			"t_node_id":set_tendermint_node_id
		}
	}

	#apply rbac createUser and createTypeInstance
	hospital_instance_rbac = createTypeInstance(namespace, admin_keys, 'hospital', hospital_type_id, user_to_mongo)
	hospital_instance_rbac_id = hospital_instance_rbac["id"]

	rbac = {
		"instance_rbac_id": hospital_instance_rbac_id
	}

	print(hospital_instance_rbac)

	#add the rbac to mongo dict
	user_to_mongo.update(rbac)
	
	#send "user" list to database
	db["hospital_accounts"].insert_one(user_to_mongo)
	
	return render_template("admin-create-hospital-result.html", content = hospital_instance_rbac)

#Routes for User
@app.route('/UserLoginPage')
def UserLoginPage():
	return render_template("user_login.html")

@app.route('/user_login', methods = ["POST"])
def user_login():
	get_email = request.form.get("email")
	get_password = request.form.get("password")
	login_cred = db["doctor_accounts"].find_one({"email":get_email})
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
			err_msg = "Login failed. Re-check your email and password."
			return render_template("error-signed-out.html",content=err_msg) 
	else:
		err_msg = "Login failed. Re-check your email and password."
		return render_template("error-signed-out.html",content=err_msg)

@app.route('/UserSignUpPage')
def showUserSignUpPage():
	return render_template("user_signup.html")

@app.route('/user_signup', methods = ["POST"])
def user_signup():
	#get credentials
	set_name = request.form.get("name")
	set_email = request.form.get("email")
	set_password = request.form.get("password")
	set_hospital = request.form.get("hospital")
	
	#verify if the email already exist on the db
	if db["doctor_accounts"].find_one({"email":set_email}):
		return jsonify({ "error": "Email address already in use" }), 400
	
	#verify if hospital exist	
	if db["hospital_accounts"].find_one({"name":set_hospital}):
		#generate keypair
		bob = generate_keypair()
		public_key = bob.public_key
		private_key = bob.private_key
		bob_keypairs = {
			'public_key': public_key,
			'private_key': private_key
		}
		
		#compile keypair and credentials into a list named "user"
		user_to_mongo = {
			"name" : set_name,
			"email" : set_email,
			"password" : set_password,
			"public_key" : public_key,
			"role" : "doctor",
			"hospital" : set_hospital
		}

		#apply rbac createUser and createTypeInstance
		doctor_user_rbac = createUser(namespace, bob_keypairs, admin_type_id, 'doctor', public_key, user_to_mongo)
		doctor_user_rbac_id = doctor_user_rbac["id"]
		print(doctor_user_rbac)
		rbac = {
			"user_rbac_id": str(doctor_user_rbac_id)
		}

		#add the rbac to mongo dict
		user_to_mongo.update(rbac)
		
		#send "user" list to database
		db["doctor_accounts"].insert_one(user_to_mongo)

		#set session
		session["role"] = "doctor"
		session["name"] = set_name
		session["public_key"] = public_key
		
		#send file
		user_to_file = {
			"user_rbac_id": str(doctor_user_rbac_id),
			"name" : set_name,
			"email" : set_email,
			"password" : set_password,
			"public_key" : public_key,
			"private_key" : private_key,
			"role" : "doctor",
			"hospital" : set_hospital
		}
		file_name = set_name+"_doctor_"+public_key+".txt"
		completedFilename = os.path.join(os.path.expanduser('~'),"medical-app/application/doctor_account",file_name)
		with open(completedFilename,'w') as file:
			file.write(json.dumps(user_to_file))
		file.close()

		#insert the rbac's createUser transaction here
		flash("Account successfully created. Return to Login Page.")
		return send_file(completedFilename, as_attachment=True)
	else:
		err_msg = "Signup failed. The Hospital you input does not exist in the database."
		return render_template("error-signed-out.html",content=err_msg)
 
#logout
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('UserLoginPage'))

#index page
@app.route('/')
def showHomePage():
	if "role" in session:
		if session["role"] == "doctor":
			welcome = "Hello! " + session["name"]
			return render_template("user_index.html", content = welcome)
		elif session["role"] == "admin":
			return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('UserLoginPage'))

#route to create
@app.route("/create-form")
def showCreatePage():
	return render_template("create-form.html",content = session["public_key"], content1 = session["name"])

@app.route("/create-result", methods = ["POST"])
def showCreateResult():
	if request.method == "POST":
		#Data untuk asset
		nik_id = str(request.form.get("nik_id"))
		print(nik_id)
		nama = str(request.form.get("nama"))
		birthplace = str(request.form.get("birthplace"))
		birthday = str(request.form.get("birthday"))
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
		public_key = request.form.get("public_key")
		doctor_name = request.form.get("doctor_name")

		#input asset dan metadata ke chain
		ns_asset = nama+"_pasien_"+nik_id

		patient_asset = {
			#rbac_shenanigans
			'patient' : {
				'nik_id' : nik_id,
				'nama' : nama,
				'ttl' : ttl,
				'jenis_kelamin' : sex,
				'alamat' : alamat,
				'gol_darah': gol_darah,
				'nama_dokter' : doctor_name,
				'id_dokter' : public_key
			},
			'ns': ns_asset,
			'link': patient_type_id
		}
		metadata = {
			'can_link':[public_key],
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
		#add asset as user
		#add asset and user as instance
		print(tx)
		return render_template("create-result.html",content=tx)
	else:
		return redirect(url_for("showCreatePage "))

#route to search
@app.route("/search-form")
def showSearchPage():
	pubkey = session["public_key"]
	return render_template("search-form.html", key = pubkey)

@app.route("/search-result", methods = ["POST","GET"])
def showSearchResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		public_key = request.form.get("public_key")
		tx = retrieve_transaction(tx_id)
		#verify can_link
		tx_can_link = tx["metadata"]["can_link"]
		if public_key in tx_can_link:
			if tx["operation"]=='TRANSFER':	
				get_prev_tx_id = tx['asset']['id']
				get_prev_tx = retrieve_transaction(get_prev_tx_id)
				tx['asset'] = get_prev_tx['asset']
				print(tx)
			else:
				print(tx)
			return render_template("search-result-success.html",content=tx)
		else:
			err_msg = "You do not have the permission to open this medical record."
			return render_template("error-landing-page.html",content=err_msg)
		
	else:
		return redirect(url_for("showSearchPage"))

#route to request access
@app.route("/search-request")
def showRequestForm():
	return render_template("search-request-form.html")

@app.route("/request", methods = ["POST","GET"])
def showRequestResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		#create a request dictionary consists of tx_id, tx's public key, and the user's public key
		user_from = session["public_key"]
		user_to = tx["asset"]["data"]["patient"]["id_dokter"]
		send_request = {
			"tx_id" : tx_id,
			"user_from" : user_from,
			"user_to": user_to,
			"status" : "request awaiting acceptance"
		}
		db["med_rec_requests"].insert_one(send_request)
		print("request from "+user_from+" has been sent to "+user_to)
		return redirect(url_for("showHomePage"))
	else:
		return redirect(url_for("showHomePage"))

#route to show table of requested tx
@app.route("/incoming-request")
def showIncomingRequestPage():
	#show list of request coming to this user
	dat = db["med_rec_requests"].find({"user_to":session["public_key"]})
	tup = []
	for y in dat:
		txs = "%s"%y["tx_id"]
		owner = "%s"%y["user_to"]
		requester = "%s"%y["user_from"]
		list = [txs,owner,requester]
		tup.append(list)
	print(tup)
	if tup:
		return render_template("incoming-request-list.html", data=tup)
	if not tup:
		err_msg = "You do not have any incoming requests to access your medical records."
		return render_template("error-landing-page.html",content=err_msg)

@app.route("/incoming-request-detail", methods = ["POST"])
def showIncomingRequestDetail():
	#get the json data of the request and print
	tx_id = request.form.get("tx_id")
	print("incoming request detail for: "+tx_id)
	requester = request.form.get("requester")
	tx = retrieve_transaction(str(tx_id))
	print(tx)
	return render_template("incoming-request-detail.html",requester=requester,id=str(tx_id),content=tx)

@app.route("/incoming_request_result", methods = ["POST"])
def incoming_request_result():
	tx_id = request.form.get("tx_id")
	print("processing incoming request for: "+tx_id)
	requester = request.form.get("requester")
	print("requested by: "+requester)

	#keypair
	private_key = request.form.get("private_key") #input name private_key
	public_key = session['public_key']
	user = {
		'public_key':public_key,
		'private_key':private_key
	}

	tx = retrieve_transaction(str(tx_id))
	tx_asset = tx['asset']
	tx_metadata = tx['metadata']
	print("================================")
	print(tx)
	tx_link = {
		'can_link':[user["public_key"], requester]
    }
	tx_metadata.update(tx_link)
	print("================================")
	print(tx_metadata)
	
	#bigchaindb processor
	updatedtx = append_transaction(tx_id, tx_asset, tx_metadata, user)
	print(updatedtx)

	#mongodb processor
	query = db["med_rec_requests"].find_one({'tx_id':tx_id},{'user_from':requester})
	print(query)
	status = "accepted. open the medical record on "+updatedtx["id"]
	data_update = {
		"$set": { 
			"status": status
		} 
	}
	db["med_rec_requests"].update_one(query, data_update)

	return render_template("incoming-request-result.html", content=tx)

#route to show table of pending tx
@app.route("/outcoming-request")
def showOutcomingRequestPage():
	#show list of request coming to this user
	dat = db["med_rec_requests"].find({"user_from":session["public_key"]})
	tup = []
	for y in dat:
		ticket_id = "%s"%y["_id"]
		txs = "%s"%y["tx_id"]
		owner = "%s"%y["user_to"]
		requester = "%s"%y["user_from"]
		status="%s"%y["status"]
		list = [ticket_id,txs,owner,requester,status]
		tup.append(list)
	print(tup)
	if tup:
		return render_template("outcoming-request-list.html", data=tup)
	if not tup:
		err_msg = "You do not have any outcoming requests to access medical records."
		return render_template("error-landing-page.html",content=err_msg)

#route to show detail of pending tx
@app.route("/outcoming-request-detail")
def showOutcomingRequestDetail():
	#show list of request coming to this user
	tx_id = request.form.get("tx_id")
	owner = request.form.get("owner")
	requester = request.form.get("requester")
	dat = db["med_rec_requests"].find({"tx_id":tx_id,"user_to":owner,"user_from":requester})
	print(dat)
	return render_template("incoming-request-list.html", data=dat)

#route to append
@app.route("/search-append")
def showSearchAppendPage():
	return render_template("search-append.html")

@app.route("/append-form", methods = ["POST","GET"])
def showAppendForm():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		#verify can_link, if can_link contains session's public key then...
		tx_can_link = tx["metadata"]["can_link"]
		if session["public_key"] in tx_can_link:
			return render_template("append-form.html",content=tx, tx_id = tx_id, key = session["public_key"], doc_name = session["name"])
		else:
			err_msg = "You do not have the permission to open this medical record."
			return render_template("error-landing-page.html",content=err_msg)
	else:
		return redirect(url_for("showSearchPage"))

@app.route("/append-result", methods = ["POST","GET"])
def showAppendResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		
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
		public_key = request.form.get("public_key")
		doctor_name = request.form.get("doctor_name")

		#input asset dan metadata ke chain
		patient_asset = {
			#rbac_shenanigans
			'patient' : {
				'nik_id' : nik_id,
				'nama' : nama,
				'ttl' : ttl,
				'jenis_kelamin' : sex,
				'alamat' : alamat,
				'gol_darah': gol_darah,
				'nama_dokter' : doctor_name,
				'id_dokter' : public_key
			}
		}
		metadata = {
			'can_link':[public_key],
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
	return render_template("search-transfer.html",pubkey = session["public_key"])

@app.route("/transfer-result", methods = ["POST"])
def showTransferResult():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_transaction(tx_id)
		address_id = request.form.get("address_id")
		private_key = request.form.get("private_key")
		public_key = request.form.get("public_key")
		user_keys = {
			"public_key":public_key,
			"private_key":private_key
		}
		meta = tx['metadata']
		tf_tx = transfer_transaction(tx,user_keys,address_id,meta)
		print(tf_tx)
		return render_template("transfer-result.html",content=tx)
	else:
		return redirect(url_for("showSearchTransferPage"))

if __name__== "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)