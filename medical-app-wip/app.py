from flask import Flask, render_template, request, redirect, url_for, sessions
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from bdb_transaction import *

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5' 

@app.route('/login')

def showLoginPage():
	return render_template("login.html")

@app.route('/signup')

def showSignUpPage():
	return render_template("signup.html")

#halaman index
@app.route('/')

def showHomePage():
	return render_template("index.html")

#route to create
@app.route("/create-form", methods = ["POST","GET"])

def showCreatePage():
	return render_template("create-form.html")

@app.route("/create-result", methods = ["POST","GET"])

def showCreateResult():
	if request.method == "POST":
		nik_id = request.form.get('nik_id')
		nama = request.form.get('nama')
		ttl = request.form.get('ttl')
		alamat = request.form.get('alamat')
		gejala = request.form.get('gejala')
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
		tx = create_medical_data(patient_asset,user_keys)
		return render_template("create-result.html",content=tx)
	else:
		return redirect(url_for("showCreatePage "))
#route to search
@app.route("/search-form", methods = ["POST","GET"])

def showSearchPage():
	return render_template("search-form.html")

@app.route("/search-result", methods = ["POST","GET"])

def showSearchResult():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		tx = retrieve_medical_data(tx_id)
		return render_template("search-result.html",content=tx)
	else:
		return redirect(url_for("showSearchPage"))

#route to append
@app.route("/search-append", methods = ["POST","GET"])

def showSearchAppendPage():
	return render_template("search-append.html")

@app.route("/append-form", methods = ["POST","GET"])
def showAppendForm():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		tx = retrieve_medical_data(tx_id)
		return render_template("append-form.html",content=tx, tx_id = tx_id)
	else:
		return redirect(url_for("showSearchPage"))

@app.route("/append-result", methods = ["POST","GET"])
def showAppendResult():
	if request.method == "POST":
		nik_id = request.form.get('nik_id')
		nama = request.form.get('nama')
		ttl = request.form.get('ttl')
		alamat = request.form.get('alamat')
		gejala = request.form.get('gejala')
		comment = request.form["comment"]
		tx_id = request.form.get('tx_id')
		patient_asset = {
			'id': tx_id,
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
		tx = update_medical_data(tx_id,patient_asset,user_keys)
		return render_template("append-result.html",content=tx)
	else:
		return redirect(url_for("showSearchAppendPage"))

#route to burn

@app.route("/search-burn", methods = ["POST","GET"])

def showSearchBurnPage():
	return render_template("search-burn.html")

@app.route("/burn-result", methods = ["POST","GET"])

def showBurn():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		tx = delete_medical_data(tx_id,user_keys)
		return render_template("burn-result.html",content=tx)
	else:
		return redirect(url_for("showSearchBurnPage"))

#route to transfer

@app.route("/search-transfer", methods = ["POST","GET"])

def showSearchTransferPage():
	return render_template("search-transfer.html")

@app.route("/transfer-result", methods = ["POST","GET"])

def showTransferResult():
	if request.method == "POST":
		tx_id = request.form["tx_id"]
		user2 = generate_keypair()
		user2_keys = {
			'public_key': user2.public_key,
			'private_key': user2.private_key
		}
		bdb_root_url = 'http://34.101.231.183:9984/'
		bdb = BigchainDB(bdb_root_url)
		tx = transfer_medical_data(bdb,tx_id,user_keys,user2_keys)
		return render_template("transfer-result.html",content=tx)
	else:
		return redirect(url_for("showSearchTransferPage"))

if __name__== "__main__":
	app.run(host='0.0.0.0', port="5000", debug=True)

