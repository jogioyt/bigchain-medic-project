from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from datetime import datetime

def create_medical_data(patient_data, user):
    bdb_root_url = 'http://34.101.231.183:9984/'
    bdb = BigchainDB(bdb_root_url)
    pub_key = user['public_key'] #temporary solution
    priv_key = user['private_key'] #temporary solution
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
    	'timestamp' : timestamp
	}
    prepared_creation_tx = bdb.transactions.prepare(
        operation = 'CREATE',
        signers = pub_key,
        asset = patient_data,
        metadata = metadata,
    )
    fulfilled_tx = bdb.transactions.fulfill(prepared_creation_tx, priv_key)
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx)
    return sent_creation_tx

def retrieve_medical_data(tx_id):
    bdb_root_url = 'http://34.101.231.183:9984/'
    bdb = BigchainDB(bdb_root_url)
    tx = bdb.transactions.retrieve(tx_id)
    return tx

def transfer_medical_data(tx_id, user1, user2):
    bdb_root_url = 'http://34.101.231.183:9984/'
    bdb = BigchainDB(bdb_root_url)
    # user1 = generate_keypair() temporary solution
    # user2 = generate_keypair() temporary solution
    user1_public_key = user1['public_key']
    user1_priv_key = user1['private_key']
    user2_public_key = user2['public_key']
    user2_priv_key = user2['private_key']
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    owners_id_before = tx['outputs'][0]['public_keys']
    transfer_input={
        'fulfillment':output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        'owners_before':owners_id_before
    }
    prepared_transfer_tx=bdb.transactions.prepare(
        operation='TRANSFER',
        asset = tx,
        inputs = transfer_input,
        recipients = user2_public_key,
    )
    fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx,user1_priv_key)
    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
    return sent_transfer_tx

def update_medical_data(tx_id, patient_data, user):
    bdb_root_url = 'http://34.101.231.183:9984/'
    bdb = BigchainDB(bdb_root_url)
    pub_key = user['public_key']
    priv_key = user['private_key']
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    owners_id_before = tx['outputs'][0]['public_keys']
    transfer_input = {
        'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        'owners_before':owners_id_before
    }
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'timestamp' : timestamp
    }
    prepared_append_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        recipients = pub_key,
        inputs = transfer_input,
        asset = patient_data,
        metadata = metadata,
    )
    fulfillAppendTransaction = bdb.transactions.fulfill(prepared_append_tx,priv_key)
    signed_append_tx = bdb.transactions.send_commit(fulfillAppendTransaction)
    return signed_append_tx

def delete_medical_data(tx_id, user):
    bdb_root_url = 'http://34.101.231.183:9984/'
    bdb = BigchainDB(bdb_root_url)
    pub_key = user['public_key']
    priv_key = user['private_key']
    tx = bdb.transactions.retrieve(tx_id)
    output = tx['outputs'][0]
    owners_id_before = tx['outputs'][0]['public_keys']
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
        'owners_before':owners_id_before,    
    }
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'timestamp' : timestamp
    }
    prepared_burn_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        asset = burn_asset,
        metadata = metadata,
        recipients=BURN_ADDRESS,
        inputs=transfer_input,
    )
    fulfillBurnTransaction = bdb.transactions.fulfill(prepared_burn_tx,priv_key)
    signed_burn_tx = bdb.transactions.send_commit(fulfillBurnTransaction)
    return signed_burn_tx
