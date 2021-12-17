from bdb_transaction import retrieve_transaction
from bigchaindb_driver import BigchainDB

bdb_root_url_1 = 'http://34.101.246.15:9984/'
bdb1 = BigchainDB(bdb_root_url_1)
bdb_root_url_2 = 'http://34.101.111.3:9984/'
bdb2 = BigchainDB(bdb_root_url_2)
bdb_root_url_3 = 'http://34.101.173.155:9984/'
bdb3 = BigchainDB(bdb_root_url_3)
bdb_root_url_4 = 'http://34.101.246.47:9984/'
bdb4 = BigchainDB(bdb_root_url_4)

def main():
    tx1_id = input("Enter the first tx_id you want to test: ")
    tx2_id = input("Enter the first tx_id you want to test: ")
    #tx3_id = input("Enter the first tx_id you want to test: ")
    #tx4_id = input("Enter the first tx_id you want to test: ")
    
    #Tx 1
    tx1_at_node1 = bdb1.transactions.retrieve(tx1_id)
    tx1_at_node2 = bdb2.transactions.retrieve(tx1_id)
    tx1_at_node3 = bdb3.transactions.retrieve(tx1_id)
    tx1_at_node4 = bdb4.transactions.retrieve(tx1_id)

    #Tx2
    tx2_at_node1 = bdb1.transactions.retrieve(tx2_id)
    tx2_at_node2 = bdb2.transactions.retrieve(tx2_id)
    tx2_at_node3 = bdb3.transactions.retrieve(tx2_id)
    tx2_at_node4 = bdb4.transactions.retrieve(tx2_id)

    #Tx3
    #tx3_at_node1 = bdb1.transactions.retrieve(tx3_id)
    #tx3_at_node2 = bdb2.transactions.retrieve(tx3_id)
    #tx3_at_node3 = bdb3.transactions.retrieve(tx3_id)
    #tx3_at_node4 = bdb4.transactions.retrieve(tx3_id)

    #Tx4
    #tx4_at_node1 = bdb1.transactions.retrieve(tx4_id)
    #tx4_at_node2 = bdb2.transactions.retrieve(tx4_id)
    #tx4_at_node3 = bdb3.transactions.retrieve(tx4_id)
    #tx4_at_node4 = bdb4.transactions.retrieve(tx4_id)

    #Verification for Transaction 1
    print("==================================")
    print("Node 1 Transaction 1")
    print("==================================")
    if (tx1_at_node1==tx1_at_node2):
        if(tx1_at_node1==tx1_at_node3):
            if(tx1_at_node1==tx1_at_node4):
                print("Transaction 1 in Node 1 is Valid")
            else:
                print("Transaction 1 in Node 1 is invalid")
        else:
            print("Transaction 1 in Node 1 is invalid")
    else:
        print("Transaction 1 in Node 1 is invalid")
    print("==================================")
    print("Node 2 Transaction 1")
    print("==================================")
    if (tx1_at_node2==tx1_at_node1):
        if(tx1_at_node2==tx1_at_node3):
            if(tx1_at_node2==tx1_at_node4):
                print("Transaction 1 in Node 2 is Valid")
            else:
                print("Transaction 1 in Node 2 is invalid")
        else:
            print("Transaction 1 in Node 2 is invalid")
    else:
        print("Transaction 1 in Node 2 is invalid")
    print("==================================")
    print("Node 3 Transaction 1")
    print("==================================")
    if (tx1_at_node3==tx1_at_node1):
        if(tx1_at_node3==tx1_at_node2):
            if(tx1_at_node3==tx1_at_node4):
                print("Transaction 1 in Node 3 is Valid")
            else:
                print("Transaction 1 in Node 3 is invalid")
        else:
            print("Transaction 1 in Node 3 is invalid")
    else:
        print("Transaction 1 in Node 3 is invalid")
    print("==================================")
    print("Node 4 Transaction 1")
    print("==================================")
    if (tx1_at_node4==tx1_at_node1):
        if(tx1_at_node4==tx1_at_node2):
            if(tx1_at_node4==tx1_at_node3):
                print("Transaction 1 in Node 4 is Valid")
            else:
                print("Transaction 1 in Node 4 is invalid")
        else:
            print("Transaction 1 in Node 4 is invalid")
    else:
        print("Transaction 1 in Node 4 is invalid")
    print("==================================")

    #Verification for Transaction 2
    print("==================================")
    print("Node 1 Transaction 2")
    print("==================================")
    if (tx2_at_node1==tx2_at_node2):
        if(tx2_at_node1==tx2_at_node3):
            if(tx2_at_node1==tx2_at_node4):
                print("Transaction 2 in Node 1 is Valid")
            else:
                print("Transaction 2 in Node 1 is invalid")
        else:
            print("Transaction 2 in Node 1 is invalid")
    else:
        print("Transaction 2 in Node 1 is invalid")
    print("==================================")
    print("Node 2 Transaction 2")
    print("==================================")
    if (tx2_at_node2==tx2_at_node1):
        if(tx2_at_node2==tx2_at_node3):
            if(tx2_at_node2==tx2_at_node4):
                print("Transaction 2 in Node 2 is Valid")
            else:
                print("Transaction 2 in Node 2 is invalid")
        else:
            print("Transaction 2 in Node 2 is invalid")
    else:
        print("Transaction 2 in Node 2 is invalid")
    print("==================================")
    print("Node 3 Transaction 2")
    print("==================================")
    if (tx2_at_node3==tx2_at_node1):
        if(tx2_at_node3==tx2_at_node2):
            if(tx2_at_node3==tx2_at_node4):
                print("Transaction 2 in Node 3 is Valid")
            else:
                print("Transaction 2 in Node 3 is invalid")
        else:
            print("Transaction 2 in Node 3 is invalid")
    else:
        print("Transaction 2 in Node 3 is invalid")
    print("==================================")
    print("Node 4 Transaction 2")
    print("==================================")
    if (tx2_at_node4==tx2_at_node1):
        if(tx2_at_node4==tx2_at_node2):
            if(tx2_at_node4==tx2_at_node3):
                print("Transaction 2 in Node 4 is Valid")
            else:
                print("Transaction 2 in Node 4 is invalid")
        else:
            print("Transaction 2 in Node 4 is invalid")
    else:
        print("Transaction 2 in Node 4 is invalid")
    print("==================================")

if __name__== "__main__":
    main()