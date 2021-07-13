from bigchaindb_driver import BigchainDB

bdb_root_url = 'http://localhost:9984/'
bdb = BigchainDB(bdb_root_url)

def create_transaction(user_keys,data_asset,meta):
    pub_key = user_keys['public_key']
    priv_key = user_keys['private_key']
    prepared_creation_tx = bdb.transactions.prepare(
        operation = 'CREATE',
        signers = pub_key,
        asset = data_asset,
        metadata = meta,
    )
    fulfilled_tx = bdb.transactions.fulfill(prepared_creation_tx, priv_key)
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_tx)
    return sent_creation_tx

def retrieve_transaction(tx_id):
    tx = bdb.transactions.retrieve(tx_id)
    return tx

def transfer_transaction(tx,user1,address_id, meta):
    # user1 = generate_keypair() temporary solution
    # user2 = generate_keypair() temporary solution
    user1_pub_key = user1["public_key"]
    user1_priv_key = user1["private_key"]
    tx_id = tx['id']
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
        recipients = address_id,
        metadata = meta
    )
    fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx,user1_priv_key)
    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
    return sent_transfer_tx

def append_transaction(tx_id,patient_data,meta,user):
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
    prepared_append_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        recipients = pub_key,
        inputs = transfer_input,
        asset = patient_data,
        metadata = meta,
    )
    fulfillAppendTransaction = bdb.transactions.fulfill(prepared_append_tx,priv_key)
    signed_append_tx = bdb.transactions.send_commit(fulfillAppendTransaction)
    return signed_append_tx

def burn_transaction(tx_id,metadata,user):
    priv_key = str(user)
    tx = bdb.transactions.retrieve(str(tx_id))
    output = tx['outputs'][0]
    owners_id_before = tx['outputs'][0]['public_keys']
    BURN_ADDRESS = "BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn"
    burn_asset = {
        "id":tx_id
    }
    transfer_input = {
        'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':tx_id,
        },
        'owners_before':owners_id_before,    
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