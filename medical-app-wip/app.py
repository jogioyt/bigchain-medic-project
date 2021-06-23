from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from flask.helpers import flash, send_file
from pymongo import collection
from bigchaindb_routes import *
from functools import wraps
import pymongo
from selenium import webdriver
import json

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5' 

#Database for account
client = pymongo.MongoClient('localhost',27017)
db = client["doctor"]
collection = db["users"]

#Login, Sign Up, and Log Out
@app.route('/showLoginPage')
def showLoginPage():
	return render_template("login.html")

@app.route('/showSignUpPage')
def showSignUpPage():
	return render_template("signup.html")

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

#route to search
@app.route("/search-form")

def showSearchPage():
	return render_template("search-form.html")

#route to append
@app.route("/search-append")

def showSearchAppendPage():
	return render_template("search-append.html")

@app.route("/append-form", methods = ["POST","GET"])
def showAppendForm():
	if request.method == "POST":
		tx_id = request.form.get("tx_id")
		tx = retrieve_medical_data(tx_id)
		return render_template("append-form.html",content=tx, tx_id = tx_id)
	else:
		return redirect(url_for("showSearchPage"))

#route to burn

@app.route("/search-burn")

def showSearchBurnPage():
	return render_template("search-burn.html")

#route to transfer

@app.route("/search-transfer")

def showSearchTransferPage():
	return render_template("search-transfer.html")

if __name__== "__main__":
	app.run(host='0.0.0.0', port="5000", debug=True)

