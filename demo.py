"""Demo script for mslreports package"""

# Import standard library packages
import os
import json

# Import dotenv for loading environment variables
from dotenv import load_dotenv

# Import MSL Reports pacakge
import mslreports

# Import specific Roles from MSLReports
from mslreports.downlink import ChemCamSPDL
from mslreports.uplink import ChemCamSPUL



#  ------------------------------------------------------



load_dotenv() # Load environment variables (username and password)

mslreports.config.username = os.getenv("JPL_USERNAME")  # Store username
mslreports.config.password = os.getenv("JPL_PASSWORD")  # Store password
mslreports.connect()  # Instantiate a requests Session to access MSLReports


rp = ChemCamSPUL.get_report(3940)

# Viewing report metadata

print('\nSol:')
print(rp.sol)

print('\nRole:')
print(rp.role)

print('\nDescription:')
print(rp.description)

print('\n', '-'*30, sep='')


# Viewing text on a report

print('\nContacts:')
print(rp.contacts)

print('\nEmail:')
print(rp.email)

print('\nDetails from Summary:')
for idx, target_details in enumerate(rp.details):
	if idx == 0:  # Just the first target
		print(json.dumps(target_details, indent=2))

print('\n', '-' * 30, sep='')


# Listing attachments on a report

print('\nAttachments:')
print(json.dumps(rp.attachments, indent=2))

print('\n', '-'*30, sep='')


# Downloading an attachment

print('\nDownloading...')
filename = rp.download_attachment("zones_LD_Kukenan_3940.jpg", 'attachments')
print('Downloaded', filename)


print('\n', '-'*30, sep='')


# Uploading an attachment

mslreports.enable_uploading()

rp_dl = ChemCamSPDL.get_report(1036)
print('\nUploading...')
filename, dest = rp_dl.upload_attachment('test-upload.txt')
print('Uploaded', filename, 'to', dest)
