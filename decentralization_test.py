#import the necessary modules which
from bdb_transaction import *
from bigchaindb_driver import BigchainDB

def createTest(user_keys,data_asset,meta):
    bdb_root_url_1 = 'http://34.101.246.15:9984/'
    bdb1 = BigchainDB(bdb_root_url_1)
    bdb_root_url_2 = 'http://34.101.111.3:9984/'
    bdb2 = BigchainDB(bdb_root_url_2)
    bdb_root_url_3 = 'http://34.101.173.155:9984/'
    bdb3 = BigchainDB(bdb_root_url_3)
    bdb_root_url_4 = 'http://34.101.246.47:9984/'
    bdb4 = BigchainDB(bdb_root_url_4)
    tx = create_transaction(user_keys,data_asset,meta)
    tx_id = tx["id"]
    tx1 = bdb1.transactions.retrieve(tx_id)
    tx2 = bdb2.transactions.retrieve(tx_id)
    tx3 = bdb3.transactions.retrieve(tx_id)
    tx4 = bdb4.transactions.retrieve(tx_id)
    if (tx1==tx2==tx3==tx4):
        status = "Decentralization test complete. The transaction has been saved in all nodes"
    else:
        status = "Test Failed."
    return status