import couchdb
from config import COUCHDB_URL, COUCHDB_ADMIN, COUCHDB_PASSWORD

# Connect to CouchDB
couch = couchdb.Server(COUCHDB_URL)
couch.resource.credentials = (COUCHDB_ADMIN, COUCHDB_PASSWORD)

# Create users database if it doesn't exist
DB_NAME = "users"
if DB_NAME not in couch:
    couch.create(DB_NAME)

db = couch[DB_NAME]
