from flask import Flask, render_template, request, redirect, url_for
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from datetime import datetime

def create_medical_data(bdb, patient_data):
	user = generate_keypair()
	pub_key = user.public_key #temporary solution
	priv_key = user.private_key #temporary solution
	now = datetime.now()
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
	metadata = {
    	'timestamp' : timestamp
	}
	prepared_creation_tx = bdb.transactions.prepare(
    	operation = 'CREATE',
    	signers = user.public_key,
    	asset = patient_data,
    	metadata = metadata,
	)
	fulfilled_tx = bdb.transactions.fulfill(prepared_creation_tx, priv_key)
	sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx)
	return sent_creation_tx

def retrieve_medical_data(bdb, tx_id):
	tx = bdb.transactions.retrieve(tx_id)
	return tx

def transfer_medical_data(bdb, tx_id, patient_data):
    user1 = generate_keypair() #temporary solution
    user2 = generate_keypair() #temporary solution
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    transfer_input={
        'fulfillment':output['condition']['details'],
        'fullfils':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        'owners_before':output['public_keys']
    }
    prepared_transfer_tx=bdb.transactions.prepare(
        operation='TRANSFER',
        asset = tx,
        input = transfer_input,
        recipients = user2.public_key,
    )
    fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx,user1.private_key)
    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
    return sent_transfer_txs

def update_medical_data(bdb, tx_id, patient_data):
    user = generate_keypair() #temporary solution
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    transfer_input = {
        'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        owners_before:output['public_keys']
    }
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'timestamp' : timestamp
    }
    prepared_append_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        asset = patient_data,
        metadata = metadata,
        inputs = transfer_input,
        recipients = user.public_key,
    )
    fulfillAppendTransaction = bdb.transactions.fulfill(prepared_append_tx,user.private_key)
    signed_append_tx = bdb.transactions.send_commit(fulfillAppendTransaction)
    return signed_append_tx

def delete_medical_data(bdb, tx_id):
    user = generate_keypair() #temporary solution
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    BURN_ADDRESS = "BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn"
    burn_asset = {
        'id':tx_id
    }
    transfer_input = {
        'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        owners_before:output['public_keys']
    }
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'timestamp' : timestamp
    }
    prepared_burn_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        asset = burn_asset,
        metadata = metadata
    )
    fulfillBurnTransaction = bdb.transactions.fulfill(prepared_burn_tx,user.private_key)
    signed_burn_tx = bdb.transactions.send_commit(fulfillBurnTransaction)
    return signed_burn_tx