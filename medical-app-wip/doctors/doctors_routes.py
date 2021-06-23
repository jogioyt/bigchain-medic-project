import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import pymongo
from bigchaindb_driver.crypto import generate_keypair
from app import app

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