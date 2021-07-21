#import the necessary modules which
from bigchaindb_driver import *
from bigchaindb_driver.crypto import generate_keypair
from rbac_methods import *
from datetime import datetime, time

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
    date = datetime.now()
    timestamp = date.strftime("%d/%m/%Y %H:%M:%S")

    #generate keypair for the creator
    admin = generate_keypair()
    admin_keys = {
		'private_key' : admin.private_key,
		'public_key' : admin.public_key
	}

    #give the app a name
    namespace = 'medical-app'

    #run the createGroup function and then retrieve the group's id
    adminGroup = createGroup(namespace,admin_keys)
    adminGroupId = adminGroup["id"]
    print("Admin Group Detail: ")
    print(adminGroup)
    print("=============================")
    print("Admin Group Id: "+adminGroupId)
    print("=============================")

    #Create Admin as User
    adminUserMetadata = {
        'event' : 'User Assigned',
        'timestamp' : timestamp,
        'publicKey' : admin_keys['public_key'],
        'eventData':{
            'userType':'admin'
        }
    }
    adminUser = createUser(namespace, admin_keys, adminGroupId, 'admin', admin_keys['public_key'], adminUserMetadata)
    adminUserId = adminUser['id']
    print("Admin User Detail: ")
    print(adminUser)
    print("=============================")
    print("Admin User Id: "+adminUserId)
    print("=============================")

    #create app representative by using createApp
    app_tx = createApp(namespace, admin_keys, adminGroupId)
    appId = app_tx["id"]
    print("App Detail: ")
    print(app_tx)
    print("=============================")
    print("App Id: "+appId)
    print("=============================")

    #Create Tribe to represent users group
    tribe1 = createType(admin_keys, namespace, 'tribe1', appId, adminGroupId)
    print("Tribe 1 details:")
    print(tribe1)
    print("=============================")
    tribe1Id = tribe1["id"]
    print("Tribe 1 Id: "+tribe1Id)
    print("=============================")

    """

    #Let's create another tribe for voting purposes
    tribe2 = createType(admin_keys, namespace, 'tribe2', appId, adminGroupId)
    print("Tribe 2 details:")
    print(tribe2)
    print("=============================")
    tribe2Id = tribe2["id"]
    print("Tribe 2 Id: "+tribe2Id)
    print("=============================")

    #Let's create another tribe for voting purposes
    tribe3 = createType(admin_keys, namespace, 'tribe3', appId, adminGroupId)
    print("Tribe 2 details:")
    print(tribe3)
    print("=============================")
    tribe3Id = tribe3["id"]
    print("Tribe 3 Id: "+tribe3Id)
    print("=============================")

    """

    #Try Creating Types that can_link to each other (for example Tribe 2's can link is into Tribe 1 etc)
    
    tribe2 = createType(admin_keys, namespace, 'hospital', appId, adminGroupId)
    print("Tribe 2 details:")
    print(tribe2)
    print("=============================")
    tribe2Id = tribe2["id"]
    print("Tribe 2 Id: "+tribe2Id)
    print("=============================")
    
    #tribe 3 correspons to tribe 2
    tribe3 = createType(admin_keys, namespace, 'doctors', appId, tribe2Id)
    print("Tribe 3 details:")
    print(tribe3)
    print("=============================")
    tribe3Id = tribe3["id"]
    print("Tribe 3 Id: "+tribe3Id)
    print("=============================")

    #tribe 4 correspons to tribe 3
    tribe4 = createType(admin_keys, namespace, 'patient', appId, tribe3Id)
    print("Tribe 4 details:")
    print(tribe4)
    print("=============================")
    tribe4Id = tribe4["id"]
    print("Tribe 4 Id: "+tribe4Id)
    print("=============================")
    
    #create user using createUser function 
    user1 = generate_keypair()
    user1_keys = {
        "private_key" : user1.private_key,
        "public_key": user1.public_key
    }
    user1Metadata = {
        'event' : 'User Assigned',
        'timestamp' : timestamp,
        'publicKey' : user1_keys['public_key'],
        'eventData':{
            'userType':'admin'
        }
    }
    user1_input = createUser(namespace, admin_keys, tribe1Id, 'tribe1', user1_keys["public_key"], user1Metadata)
    print("User 1 details:")
    print(user1_input)
    print("=============================")
    user1Id = user1_input["id"]
    print("User 1 Id: "+user1Id)
    print("=============================")

    #let's try to make another user
    user2 = generate_keypair()
    user2_keys = {
        "private_key" : user2.private_key,
        "public_key": user2.public_key
    }
    user2Metadata = {
        'event' : 'User Assigned',
        'timestamp' : timestamp,
        'publicKey' : user1_keys['public_key'],
        'eventData':{
            'userType':'admin'
        }
    }
    user2_input = createUser(namespace, admin_keys, tribe1Id, 'tribe2', user2_keys["public_key"], user2Metadata)
    print("User 2 details:")
    print(user2_input)
    print("=============================")
    user2Id = user2_input["id"]
    print("User 2 Id: "+user2Id)
    print("=============================")

    user3 = generate_keypair()
    user3_keys = {
        "private_key" : user3.private_key,
        "public_key": user3.public_key
    }
    user3Metadata = {
        'event' : 'User Assigned',
        'timestamp' : timestamp,
        'publicKey' : user1_keys['public_key'],
        'eventData':{
            'userType':'admin'
        }
    }
    user3_input = createUser(namespace, admin_keys, tribe1Id, 'tribe2', user3_keys["public_key"], user3Metadata)
    print("User 3 details:")
    print(user3_input)
    print("=============================")
    user3Id = user3_input["id"]
    print("User 3 Id: "+user3Id)
    print("=============================")

    """
    instance test case
    Set the permissions for each tribe
    """
    tribe1_proposal = createType(admin_keys, namespace, 'proposal', appId, tribe1Id)
    tribe2_vote = createType(admin_keys, namespace, 'vote', appId, tribe2Id)

    tribe1_proposal_id = tribe1_proposal["id"]
    tribe2_vote_id = tribe2_vote["id"]

    print("Tribe 1 details as Proposal:")
    print(tribe1_proposal)
    print("=============================")
    print("Proposal_Tribe1 Id: "+tribe1_proposal_id)
    print("=============================")
    
    print("Tribe 2 details as Vote:")
    print(tribe2_vote)
    print("=============================")
    print("Vote_Tribe2 Id: "+tribe2_vote_id)
    print("=============================")

    #Test Case

    #set proposal to user 1 - should pass
    user1_as_proposal_metadata ={
        'name':'new proposal by user 1',
        'timestamp':timestamp
    }
    user1_as_proposal = createTypeInstance(namespace, user1_keys, 'proposal', tribe1_proposal_id, user1_as_proposal_metadata)
    
    #set vote to user 2 - should pass
    user2_as_vote_metadata ={
        'name':'new vote by user 2',
        'timestamp':timestamp
    }
    user2_as_vote = createTypeInstance(namespace, user2_keys, 'vote', tribe2_vote_id, user2_as_vote_metadata)

    #set proposal to user 3 - should pass
    user3_as_proposal_metadata ={
        'name':'new proposal by user 3',
        'timestamp':timestamp
    }
    user3_as_proposal = createTypeInstance(namespace, user3_keys, 'proposal', tribe1_proposal_id, user3_as_proposal_metadata)

    #set vote to user 1 - should fail
    user1_as_vote_metadata = {
        'name':'new vote by user 1',
        'timestamp':timestamp
    }
    user1_as_vote = createTypeInstance(namespace, user1_keys, 'vote', tribe2_vote_id, user1_as_vote_metadata)

    #try printing all the proposal and vote
    print("Proposal by User 1: ")
    print(user1_as_proposal)
    print("=============================")
    print("User 1 Proposal Id: "+user1_as_proposal["id"])
    print("=============================")
    print("Vote by User 2: ")
    print(user2_as_vote)
    print("=============================")
    print("User 2 Vote Id: "+user2_as_vote["id"])
    print("=============================")
    print("Proposal by User 3: ")
    print(user3_as_proposal)
    print("=============================")
    print("User 3 Proposal Id: "+user3_as_proposal["id"])
    print("=============================")
    print("Vote by User 1: ")
    print(user1_as_vote)
    print("=============================")
    print("User 1 Vote Id: "+user1_as_vote["id"])
    print("=============================")

if __name__== "__main__":
    main()