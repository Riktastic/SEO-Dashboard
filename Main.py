import configparser
import json

# Import database scripts
from lib_database import get_dbs, get_database, get_collection, insert_collection 

from lib_google_analytics import ga_initialize, ga_convert_response_to_dict, ga_get_report_site



#Open "Settings.ini". Haal hieruit de instellingen en koppel deze aan variabelen. https://docs.python.org/3.4/library/configparser.html
config_filename = "Settings.ini"
config = configparser.ConfigParser()
config.read(config_filename)

# DB variables
config_databaseserver_host = str(config['Databaseserver']['Host'])
config_databaseserver_port = str(config['Databaseserver']['Port'])
config_databaseserver_database = str(config['Databaseserver']['Database'])

hostname = 'rik_heijmann_com'

def main():
    dbs = get_dbs(config_databaseserver_host, config_databaseserver_port)
    ga = ga_initialize()
    

    #### Google Analytics: Site rapportage
    print("1. Google Analytics: Site rapportage")
    #Opruimen:
    collection = None
    response = None
    response_converted = None
    # Open de juiste collection.
    collection = get_collection(dbs, config_databaseserver_database, str(hostname + "_ga_site"))
    # Voer de query uit. En vang de response op.
    response = lib_google_analytics.ga_get_report_site(ga)
    # Converteer de response naar BSON.
    response_converted = ga_convert_response_to_dict(response)
    # Controleer of dat het conversie proces gelukt is.
    if response_converted != False:
        # Importeer de geconverteerde response naar de MongoDB-collection.
        collection.insert_many(response_converted)
    ####


    #### Google Analytics: Pagina rapportage
    print("2. Google Analytics: Pagina rapportage")
    # Opruimen:
    collection = None
    response = None
    response_converted = None
    # Open de juiste collection.
    collection = get_collection(dbs, config_databaseserver_database, str(hostname + "_ga_pages"))
    # Voer de query uit. En vang de response op.
    response = lib_google_analytics.ga_get_report_pages(ga)
    # Converteer de response naar BSON.
    response_converted = ga_convert_response_to_dict(response)
    # Controleer of dat het conversie proces gelukt is.
    if response_converted != False:
        # Importeer de geconverteerde response naar de MongoDB-collection.
        collection.insert_many(response_converted)
    ####

    #### Google Analytics: Leeftijds rapportage
    print("3. Google Analytics: Leeftijds rapportage")
    # Opruimen:
    collection = None
    response = None
    response_converted = None
    # Open de juiste collection.
    collection = get_collection(dbs, config_databaseserver_database, str(hostname + "_ga_users_age"))
    # Voer de query uit. En vang de response op.
    response = lib_google_analytics.ga_get_report_users_age(ga)
    # Converteer de response naar BSON.
    response_converted = ga_convert_response_to_dict(response)
    # Controleer of dat het conversie proces gelukt is.
    if response_converted != False:
        # Importeer de geconverteerde response naar de MongoDB-collection.
        collection.insert_many(response_converted)
    ####


    #### Google Analytics: Land rapportage
    print("4. Google Analytics: Land rapportage")
    # Opruimen:
    collection = None
    response = None
    response_converted = None
    # Open de juiste collection.
    collection = get_collection(dbs, config_databaseserver_database, str(hostname + "_ga_users_country"))
    # Voer de query uit. En vang de response op.
    response = lib_google_analytics.ga_get_report_users_country(ga)
    # Converteer de response naar BSON.
    response_converted = ga_convert_response_to_dict(response)
    # Controleer of dat het conversie proces gelukt is.
    if response_converted != False:
        # Importeer de geconverteerde response naar de MongoDB-collection.
        print(response_converted)
        for i in response_converted:
            
        collection.insert_many(response_converted)
    ####


    #### Google Analytics: Geslacht rapportage
    print("5. Google Analytics: Geslacht rapportage")
    # Opruimen:
    collection = None
    response = None
    response_converted = None
    # Open de juiste collection.
    collection = get_collection(dbs, config_databaseserver_database, str(hostname + "_ga_users_gender"))
    # Voer de query uit. En vang de response op.
    response = lib_google_analytics.ga_get_report_users_gender(ga)
    # Converteer de response naar BSON.
    response_converted = ga_convert_response_to_dict(response)
    # Controleer of dat het conversie proces gelukt is.
    if response_converted != False:
        # Importeer de geconverteerde response naar de MongoDB-collection.
        collection.insert_many(response_converted)

if __name__ == '__main__':
  main()