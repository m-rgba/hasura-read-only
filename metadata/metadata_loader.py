import json
import requests
import os
from datetime import datetime

# Get 'now'
now = "{:%m%d%Y_%H%M%S}".format(datetime.now())

# Check health of API
hasura_url = os.getenv('HASURA_URL')

while True:
  print('❤️ Checking API Health')
  print('Checking health for: ' + hasura_url)
  health_res = requests.get(hasura_url + "/healthz")
  if health_res.status_code != 200:
    print('💔 Healthcheck Failed. Retrying...')
    continue
  else:
    print('✅ Healthcheck Succeeded')
    break

# Add response headers
headers = {
  "x-hasura-admin-secret": os.getenv('HASURA_GRAPHQL_ADMIN_SECRET'),
  "Content-type": "application/json"
}
# Setup backup payload
backup_payload = {
  "type" : "export_metadata",
  "version": 2,
  "args": {}
}

# Make backup of current metadata - alleviate oopsies
try:
  print('📂 Running Backup...')
  backup_res = requests.post(
    hasura_url + "/v1/metadata",
    headers=headers,
    json=backup_payload
  )
  with open("/metadata/backups/" + now + "_metadata.json", "w") as f:
    f.write(backup_res.text) 
    print('✅ Backup saved as: /metadata/backups/' + now + '_metadata.json')
except Exception as e:
  print('❌ Metadata backup failed.')
  raise Exception(e)

# Backup response
if backup_res.status_code == 200:
  print('✅ Metadata backup successful.')
elif backup_res.status_code >= 400:
  print('❌ There was a problem backing up your metadata.')
  raise Exception(import_res.text)
else:
  print('❌ There was a problem backing up your metadata.')
  raise Exception(import_res.text)

# Load metadata file
metadata = open('/metadata/metadata.json')
try:
  metadata_data = json.load(metadata)
  print('🚀 Metadata to Load:')
  print(metadata_data['metadata'])
except Exception as e:
  print('❌ Parsing metadata failed.')
  raise Exception(e)

# Setup import payload
import_payload = {
  "type" : "replace_metadata",
  "version": 2,
  "args": {
    "allow_inconsistent_metadata": True,
    "metadata": metadata_data['metadata']
  }
}
    
# Import metadata
try:
  import_res = requests.post(
    hasura_url + "/v1/metadata",
    headers=headers,
    json=import_payload
  )
except Exception as e:
  print('❌ Metadata import request failed.')
  raise Exception(e)

# Import response
if import_res.status_code == 200:
  print('✅ Metadata loaded successfully!')
  print(import_res.text)
elif import_res.status_code >= 400:
  print('❌ There was a problem loading your metadata.')
  raise Exception(import_res.text)
else:
  print('❌ There was a problem loading your metadata.')
  raise Exception(import_res.text)