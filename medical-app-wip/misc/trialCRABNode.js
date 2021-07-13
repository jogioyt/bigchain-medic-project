
const driver = require('bigchaindb-driver')
const { default: connection } = require('bigchaindb-driver/dist/node/connection')
const { default: transaction } = require('bigchaindb-driver/dist/node/transaction')


// BigchainDB server instance (e.g. https://example.com/api/v1/)
const API_PATH = 'http://localhost:9984/'

const conn = new driver.Connection(API_PATH)

// Create a new keypair.
const alice = new driver.Ed25519Keypair()
const bob = new driver.Ed25519Keypair()

// Asset Data Example
const assetdata = {
    'patientA' : {
        'id_number' : "rs001-01",
        'patient_name' : "John Doe",
        'patient_div' : 'radiology'
    }
}

// Metadata Example
metadata = {
    'symptoms' : 'fever caused by complication',
    'medication' : 'CT-Scan'
}

// Construct a transaction payload

console.log("====================Create Transaction==========================")

const assetCreateTx = driver.Transaction.makeCreateTransaction(
    assetdata,
    metadata,
   // Every transaction which you make requires an output
    [ driver.Transaction.makeOutput( driver.Transaction.makeEd25519Condition(alice.publicKey))
    ],
    alice.publicKey
)

// Sign the transaction with private keys
const assetCreateTxSigned = driver.Transaction.signTransaction(assetCreateTx, alice.privateKey)
conn.postTransactionCommit(assetCreateTxSigned)
assetCreateTxSigned_id = assetCreateTxSigned.id
console.log("Transact ID is: ",assetCreateTxSigned_id)

/* Transfer Transaction

console.log("====================Transfer Transaction==========================")

const assetTransferTx = driver.Transaction.makeTransferTransaction(
    [{ tx: assetCreateTxSigned, output_index: 0 }],
    [driver.Transaction.makeOutput(driver.Transaction.makeEd25519Condition(bob.publicKey))],
);

Sign the transaction with private keys

const assetTransferTxSigned = driver.Transaction.signTransaction(assetTransferTx, alice.privateKey)
conn.postTransactionCommit(assetTransferTxSigned)
assetTransferTxSigned_id = assetTransferTxSigned.id
console.log("Patient Data transfer to Bob is successful. Transact ID is: ",assetTransferTxSigned_id)
console.log('Is Bob the owner?', assetTransferTxSigned['outputs'][0]['public_keys'][0] == bob.publicKey)
*/

/* Append (similar to update; Depend on Transfer Tx)

console.log("====================Append Operation==========================")

newMetadata = {
    'symptoms' : 'Update 1 - complication reduced',
    'medication' : 'Update 1 - 1 week hospital care'
}

const appendTransaction = driver.Transaction.makeTransferTransaction(
    [{ tx: assetCreateTxSigned, output_index: 0 }],
    [driver.Transaction.makeOutput(driver.Transaction.makeEd25519Condition(alice.publicKey))],
    //modified metadata
    newMetadata
    );
    
const SignedAppend = driver.Transaction.signTransaction(appendTransaction, alice.privateKey)
conn.postTransactionCommit(SignedAppend)
SignedAppend_id = SignedAppend.id
console.log("An update on an asset is succesful. Transact ID is: ",SignedAppend_id)
*/

/* Burn (similar to delete; Depend on Transfer Tx)

console.log("====================Burn Operation==========================")

const BURN_ADDRESS = 'BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn'

const burnTransaction = driver.Transaction.makeTransferTransaction(
    [{ tx: assetCreateTxSigned, output_index: 0 }],
    [driver.Transaction.makeOutput(
        driver.Transaction.makeEd25519Condition(BURN_ADDRESS))
    ],
    {'status':'Burned'}
    );

const SignedBurn = driver.Transaction.signTransaction(burnTransaction, alice.privateKey)
conn.postTransactionCommit(SignedBurn)
SignedBurn_id = SignedBurn.id
console.log("An update to burn an asset is succesful. Transact ID is: ",SignedBurn_id)
*/

/*
function retrieveTx(txid) {
    return new Promise(function(resolve, reject) {
        conn.searchAssets(txid).then(retrievedTx => {
            var data = {};
            data.assetdata = retrievedTx[0];
            getSortedTransactions(txid).then(metadata => {
                if (isArray(metadata)) {
                    data.metadata = metadata[0].metadata;
                }
                else {
                    data.metadata = metadata;
                }
                resolve(data);
            });
        }).catch(err => {
            reject(new Error(err));
        });
    });
}

function isArray(what){
    return Object.prototype.toString.call(what) === '[object Array]';
}

function getSortedTransactions(assetId){
    var metaData = {}
    return connection.listTransactions(assetId)
        .then((txList) => {
            if (txList.length <= 1){
                return txList
            }
            const inputTransactions = []
            txList.forEach((tx) => {
                for (var key in tx.metadata){
                    metaData[key] = tx.metadata[key];
                }
            }
            )
            return metaData;
        });
}

console.log(retrieveTx(assetCreateTxSigned_id))
*/

console.log("=====================================================")