#import the necessary modules which
from bigchaindb_driver import *
from bigchaindb_driver.crypto import generate_keypair
from try_rbac_methods import *
import datetime

"""
inititate users for this role based shenanigans
1. creator = the user that would then create id for the app

"""
def main():
    """
    #Since this is python, we use asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    """
    
    #generate keypair for the creator
    creator = generate_keypair()
    creator_keys = {
		'private_key' : creator.private_key,
		'public_key' : creator.public_key
	}

    #give the app a name
    namespace = 'rbac-bdb-demo'

    #run the createGroup function and then retrieve the group's id
    adminGroup = createGroup(namespace,creator_keys)
    adminGroupId = adminGroup["id"]
    print("AdminGroup: "+adminGroupId)

    #create app representative by using createApp
    app_tx = createApp(namespace, creator_keys, adminGroupId)
    appId = app_tx["id"]
    print("App: "+appId)

    #Create Tribe to represent users group
    tribe1 = createType(creator_keys, namespace, 'tribe1', appId, adminGroupId)
    print("Tribe 1 details:")
    print(tribe1)
    tribe1Id = tribe1["id"]

    #create user instances
    user1 = generate_keypair()
    user1_keys = {
        "private_key" : user1.private_key,
        "public_key": user1.public_key
    }
    user1_input = createUser(namespace, creator_keys, tribe1Id, 'tribe1', user1_keys["public_key"])
    print("User 1 details:")
    print(user1_input)

if __name__== "__main__":
    main()