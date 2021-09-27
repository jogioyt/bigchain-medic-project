#import the necessary modules which
from bigchaindb_driver import *
from datetime import datetime
from bdb_transaction import create_transaction, transfer_transaction

#function to create identifier for the app
def createGroup(namespace, admin_keys):
    ns = namespace+'.admin'
    adminGroupAsset = {
        'data':{
            'ns':ns,
            'name': 'admin'
        }
    }
    adminGroupMetadata = {
        'can_link' : admin_keys['public_key']
    }
    adminGroup = create_transaction(admin_keys, adminGroupAsset, adminGroupMetadata)
    return adminGroup

def createApp(namespace, admin_keys, adminGroupId):
    appAsset = {
        'data': {
            'ns' : namespace,
            'name' : namespace
        }
    }
    appMetadata = {
        'can_link' : adminGroupId
    }
    app_tx = create_transaction(admin_keys, appAsset, appMetadata)
    return app_tx

#function createUser
def createUser(namespace, adminKeyPair, userTypeId, userTypeName, userPublicKey, userMetadata):
    ns_asset = namespace+"."+userTypeName 
    asset = {
        'data':{
            'ns': ns_asset,
            'link' : userTypeId,
            'createdBy': adminKeyPair["public_key"],
            'type' : userTypeName,
            'keyword':'UserAsset'          
        }
    }
    date = datetime.now()
    timestamp = date.strftime("%d/%m/%Y %H:%M:%S")
    metadata = {
        'event':'User Added',
        'timestamp': timestamp,
        'publicKey' : adminKeyPair["public_key"],
        'eventData':{
            'userType':userTypeName
        }
    }
    instanceTx = create_transaction(adminKeyPair, asset, metadata)
    transfer_transaction(instanceTx, adminKeyPair,userPublicKey, userMetadata)
    return instanceTx

#function create type
def createType(adminKeys, namespace, typeName, appId, canLinkAssetId):
    ns_asset = namespace+"."+typeName
    asset = {
        'data':{
            'ns': ns_asset,
            'link': appId,
            'name': typeName
        }
    }
    metadata = {
        'can_link': canLinkAssetId
    }
    typeTx = create_transaction(adminKeys, asset, metadata)
    return typeTx

#function create type instance that are being used setting an user to become either "proposal" or "vote"
def createTypeInstance(namespace, keypair, typeName, typeId, instanceMetadata):
    ns_asset = namespace+"."+typeName
    asset = {
        'data':{
            'ns' : ns_asset,
            'link' : typeId
        }
    }
    tx = create_transaction(keypair, asset, instanceMetadata)
    return tx