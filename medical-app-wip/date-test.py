"""
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)	
"""
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

user = generate_keypair()

print(user)