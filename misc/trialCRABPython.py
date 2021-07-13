# Inisiasi Bigchain
from bigchaindb_driver import BigchainDB

# generate keypair
from bigchaindb_driver.crypto import generate_keypair

bdb_root_url = 'http://34.101.190.101:9984/'

bdb = BigchainDB(bdb_root_url)

alice = generate_keypair()
bob = generate_keypair()


# contoh asset data untuk block

id_number = input("Masukkan nomor nomor id: ")
patient_name = input("Masukkan nama pasien: ")
symptoms = input("Masukkan gejala: ")
division = input("Masukkan divisi RS: ")
medication = input("Masukkan resep obat: ")
comment = input("(Opsional) Masukkan Komentar: ")

patient = {
    'data' : {
        'patient' : {
            'id_number' : id_number,
            'patient_name': patient_name,
            'symptoms' : symptoms,
            'division' : division,
            'medication' : medication
        },
    },
}

# contoh metadata untuk asset block
metadata = {
    'comment' : comment
}

#CREATE

prepared_creation_tx = bdb.transactions.prepare(
    operation = 'CREATE',
    signers = alice.public_key,
    asset = patient,
    metadata = metadata,
)

# print("the content of this transaction: ",prepared_creation_tx)

fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys = alice.private_key)

sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

signed_tx = sent_creation_tx

signed_tx_id = sent_creation_tx['id']

print("===============================================================")
print("Data anda sudah berhasil diunggah. ID data anda: ",signed_tx_id)
print("===============================================================")

# print("Isi transaksi yang sudah signed: ",signed_tx)

# block_height = bdb.blocks.get(signed_tx['id'])

# print(block_height)

# block = bdb.blocks.retrieve(str(block_height))

# print(block) 

answer1 = input("Do you want to try to transfer your transaction? (y/n) : ")
if(answer1 == "y"):
    get_transaction_id = input("Enter the transaction ID you want to update: ")
    creation_tx = bdb.transactions.retrieve(get_transaction_id)
    output = creation_tx['outputs'][0]
    
    transfer_input = {
        'fulfillment' : output['condition']['details'],
        'fulfills':{
            'output_index':0,
            'transaction_id':get_transaction_id,
        },
        'owners_before': output['public_keys'],
    }

    transfer_asset = {
        'id' : get_transaction_id,
        'data' : {
            'patient' : {
                'id_number' : id_number,
                'patient_name': patient_name,
                'symptoms' : symptoms,
                'division' : division,
                'medication' : medication
            },
        },
    }

    prepared_transfer_tx = bdb.transactions.prepare(
        operation = 'TRANSFER',
        asset = transfer_asset,
        inputs = transfer_input,
        recipients= bob.public_key,
    )

    fulfilled_transfer_tx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys = alice.private_key,
    )

    sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)

    signed_tx2 = sent_transfer_tx

    signed_tx2_id = sent_transfer_tx['id']

    print("Data anda berhasil di Transfer. ID Transaksi Transfer: ", signed_tx2_id)
    print("===============================================================")
else:
    answer2 = input("Do you want to try to update your transaction? (y/n) : ")
    print("===============================================================")

    if(answer2 == "y"):
        get_transaction_id = input("Enter the transaction ID you want to update: ")

        get_tx = bdb.transactions.retrieve(get_transaction_id)
    
        id_number = input("Masukkan nomor nomor id: ")
        patient_name = input("Masukkan nama pasien: ")
        symptoms = input("Masukkan gejala: ")
        division = input("Masukkan divisi RS: ")
        medication = input("Masukkan resep obat: ")
        comment = input("(Opsional) Masukkan Komentar: ")

        transfer_asset = {
            'id' : get_transaction_id,
            'data' : {
                'patient' : {
                    'id_number' : id_number,
                    'patient_name': patient_name,
                    'symptoms' : symptoms,
                    'division' : division,
                    'medication' : medication
                },
            },
        }

        metadata = {
            'comment' : comment
        }

        
        output = get_tx['outputs'][0]
        
        transfer_input = {
            'fulfillment' : output['condition']['details'],
            'fulfills':{
                'output_index':0,
                'transaction_id':get_transaction_id,
            },
        '   owners_before': output['public_keys'],
        }
        
        prepared_append_tx = bdb.transactions.prepare(
            operation = 'TRANSFER',
            asset = transfer_asset,
            metadata = metadata,
            inputs = transfer_input,
            recipients= alice.public_key,
        )

        fulfillAppendTransaction = bdb.transactions.fulfill(
            prepared_append_tx, 
            private_keys=alice.private_key,
        )

        signed_append_tx = bdb.transactions.send_commit(fulfillAppendTransaction)

        signed_append_txid = signed_append_tx['id']

        print("Data anda berhasil di Append. ID Transaksi Transfer: ", signed_append_txid)

    else:
        answer3 = input("Do you want to try to burn it instead? (y/n) : ")
        if (answer3=="y"):
            get_transaction_id = input("Enter the transaction ID you want to update: ")

            get_tx = bdb.transactions.retrieve(get_transaction_id)
        
            BURN_ADDRESS = "BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn"

            transfer_asset = {
                'id': get_transaction_id,
            }

        
        
            output = get_tx['outputs'][0]
        
            transfer_input = {
                'fulfillment' : output['condition']['details'],
                'fulfills':{
                    'output_index':0,
                    'transaction_id':get_transaction_id,
                },
                'owners_before': output['public_keys'],
            }
        
            prepared_burn_tx = bdb.transactions.prepare(
                operation = 'TRANSFER',
                asset = transfer_asset,
                inputs = transfer_input,
                recipients= BURN_ADDRESS,
            )

            fulfillBurnTransaction = bdb.transactions.fulfill(
                prepared_burn_tx, 
                private_keys=alice.private_key,
            )

            signed_burn_tx = bdb.transactions.send_commit(fulfillBurnTransaction)

            signed_burn_txid = signed_burn_tx['id']

            print("Data anda berhasil di Burn. ID Transaksi Transfer: ", signed_burn_txid)

print("===============================================================")
