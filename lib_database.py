# ### Libraries:
# Voor het uitvoeren van shell commando's:
import pymongo
import configparser
import string
import json

#Open "Settings.ini". Haal hieruit de instellingen en koppel deze aan variabelen. https://docs.python.org/3.4/library/configparser.html
config_filename = "Settings.ini"
config = configparser.ConfigParser()
config.read(config_filename)

def get_dbs(host,port):    
   # Maak verbinding met de MongoDB-server. https://www.w3schools.com/python/python_mongodb_create_db.asp
   client = pymongo.MongoClient("mongodb://{}:{}/".format(host, port))
   return client;

def get_database(client, database):
    # Selecteert/Maakt een database aan.
    return client[database]

def get_database_check(client, database):
    # Controleert of dat de opgegeven database bestaat.
    # Voorbeeld: print(DB_Database_Check(client, "OneSquad_eu"))
    dblist = client.list_database_names()
    if database in dblist:
        return True
    else:
        return False
    
def get_collection(client, database, collection):
    # Selecteert/Maakt recursief een collection aan. En ook de datbase indien die niet bestaat.
    client_database = client[database]
    return client_database[collection]

def insert_collection(collection, document):
    # Selecteert/Maakt recursief een collection aan. En ook de datbase indien die niet bestaat.
    collection.insert_many(document)


def check_collection(client, database, collection):
    # Controleert of dat de opgegeven collection bestaat.
    # Voorbeeld: print(DB_Collection_Check(client, "OneSquad_eu", "test"))
    db_instance = DB_Database(client, database)
    collection_list = db_instance.list_collection_names()
    if collection in collection_list:
        return True
    else:
        return False