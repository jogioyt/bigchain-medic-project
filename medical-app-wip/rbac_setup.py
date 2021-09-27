#import the necessary modules which
from bdb_transaction import retrieve_transaction
from bigchaindb_driver import *
from bigchaindb_driver.crypto import generate_keypair
from rbac_methods import *
from datetime import datetime, time
import json

"""
inititate users for this role based shenanigans
1. creator = the user that would then create id for the app

"""
def getAdminType():
    filename = "admin-type.txt"
    with open(filename) as json_file:
        data = json.load(json_file)
        assetId = data["id"]
    json_file.close()
    return assetId

def getApp():
    filename = "app.txt"
    with open(filename) as json_file:
        data = json.load(json_file)
        assetId = data["id"]
    json_file.close()
    return assetId

def getHospitalType():
    filename = "hospital-type.txt"
    with open(filename) as json_file:
        data = json.load(json_file)
        assetId = data["id"]
    json_file.close()
    return assetId

def getDoctorType():
    filename = "doctor-type.txt"
    with open(filename) as json_file:
        data = json.load(json_file)
        assetId = data["id"]
    json_file.close()
    return assetId

def getPatientType():
    filename = "patient-type.txt"
    with open(filename) as json_file:
        data = json.load(json_file)
        assetId = data["id"]
    json_file.close()
    return assetId

def main():
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

    file_name1 = "admin-type.txt"
    with open(file_name1,'w') as file:
        file.write(json.dumps(adminGroup))
    file.close()

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

    file_name2 = "app.txt"
    with open(file_name2,'w') as file2:
        file2.write(json.dumps(app_tx))
    file2.close()

    #Try Creating Types that can_link to each other (for example Tribe 2's can link is into Tribe 1 etc)

    hospital_type = createType(admin_keys, namespace, 'hospital', appId, adminGroupId)
    print("Hospital Type details:")
    print(hospital_type)
    print("=============================")
    hospital_type_id = hospital_type["id"]
    print("Hospital Type Id: "+hospital_type_id)
    print("=============================")

    file_name3 = "hospital-type.txt"
    with open(file_name3,'w') as file3:
        file3.write(json.dumps(app_tx))
    file3.close()

    #tribe 3 correspons to tribe 2
    doctor_type = createType(admin_keys, namespace, 'doctors', appId, hospital_type_id)
    print("Doctor type details:")
    print(doctor_type)
    print("=============================")
    doctor_type_id = doctor_type["id"]
    print("Doctor type Id: "+ doctor_type_id)
    print("=============================")

    file_name4 = "doctor-type.txt"
    with open(file_name4,'w') as file4:
        file4.write(json.dumps(app_tx))
    file4.close()

    #tribe 4 correspons to tribe 3
    patient_type = createType(admin_keys, namespace, 'patient', appId, doctor_type_id)
    print("Patient type details:")
    print(patient_type)
    print("=============================")
    patient_type_id = patient_type["id"]
    print("Patient type Id: "+patient_type_id)
    print("=============================")

    file_name5 = "doctor-type.txt"
    with open(file_name5,'w') as file5:
        file5.write(json.dumps(app_tx))
    file5.close()

if __name__== "__main__":
    main()