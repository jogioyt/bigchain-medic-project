#import the necessary modules which
from bigchaindb_driver import *
from bigchaindb_driver.common.transaction import Transaction
from bigchaindb_driver.crypto import generate_keypair
from bdb_transaction import *
from datetime import datetime

#initiate connection to the BigchainDB server
bdb_root_url = "http://localhost:9984"
bdb = BigchainDB(bdb_root_url)

#function to create identifier for the app
def createApp():
    admin_keys = generate_keypair()
    namespace = "rbac-bdb-py-tutorial"
    adminGroupAsset = {
        'ns': 'rbac-bdb-py-tutorial.admin',
        'name' : 'admin'
    }
    adminGroupMetadata = {
        'canLink' : admin_keys.public_key
    }
    adminGroup = create_transaction(admin_keys, adminGroupAsset, adminGroupMetadata)
    adminGroupID = adminGroup.id
    appAsset = {
        'ns' : namespace,
        'name' : namespace
    }
    appMetadata = {
        'canLink' : adminGroupID
    }
    app_tx = create_transaction(admin_keys, appAsset, appMetadata)
    appID = app_tx.id

    return appID

#function createUser
def createUser(adminKeyPair, userTypeId, userTypeName, userPublicKey, userMetadata):
    namespace = 'rbac-bdb-py-tutorial.admin'
    ns_asset = namespace+"."+userTypeName
    asset = {
        'ns': ns_asset,
        'link' : userTypeId,
        'createdBy': adminKeyPair.public_key,
        'type' : userTypeName,
        'keyword':'UserAsset'
    }
    date = datetime.now()
    timestamp = date.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'event':'User Added',
        'date' : date,
        'timestamp': timestamp,
        'publicKey' : adminKeyPair.public_key,
        'eventData':{
            'userType':userTypeName
        }
    }
    instanceTx = create_transaction(adminKeyPair, asset, metadata)
    transfer_transaction(instanceTx, adminKeyPair,userPublicKey, userMetadata)
    return instanceTx

#function create type
def createType(admin1, typeName, appId, canLinkAssetId):
    namespace = 'rbac-bdb-py-tutorial.admin'
    ns_asset = namespace+"."+typeName
    asset = {
        'ns': ns_asset,
        'link': appId,
        'name' : typeName

    }
    metadata = {
        'can_link': canLinkAssetId
    }
    typeTx = create_transaction(admin1, asset, metadata)
    return typeTx

#function create type instance that are being used setting an user to become either "proposal" or "vote"
def createTypeInstance(keypair, typeName, typeId, metadata):
    namespace = 'rbac-bdb-py-tutorial.admin'
    ns_asset = namespace+"."+typeName
    asset = {
        'ns' : ns_asset,
        'link' : typeId
    }
    tx = create_transaction(keypair, asset, metadata)
    return tx