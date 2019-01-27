# The module uses a random number generator to get 15 random Star Wars characters from the
# SWAPI endpoint. For each of the 15 characters retreived, the module will write new records to a
# MySQL database with the names of the Star Wars films that character has appeared in.
# The films and a list of their characters will be written to a Python dictionary and printed
# to the console as JSON.

# Flow of control for the module is maintained in the main() function

# Import 'requests' and 'json' libraries to perform API calls and manipulate JSON data
# Import 'random' library to generate random integer to be used in API call
# Import 'mysql' modules to interact with a local MySQL database
# Import 'getpass' to hide user input when typing a password into the console
# Import 'jsbeautifier' to format JSON for console output readability
import json
import random
import getpass
import jsbeautifier
import requests
import mysql.connector
from mysql.connector import errorcode



# Base URL endpoint for Star Wars characters API
BASE_URL = 'https://swapi.co/api/people/'

# MySQL Database variables
# TABLES holds SQL commands for inserting new tables
DB_NAME = 'swapi_db'
TABLES = {}

# List to hold films and associated characters
# Dictionary keys are episode IDs. Each episode has a nested dict containing the film title and
# a list of characters that appeared in that film.
FILMS = {}



# Generates a random number between 1 and 87 and appends it to the base people API URL
def getRandomIntAndAppend():
    url = BASE_URL
    while True:
        random_int = random.randint(1,88)
        # While system testing, found that person 17 throws a 404 error
        if random_int == 17:
            continue 
        else:
            url += str(random_int)
            break
    return url



# Gets random numbers and appends them to base_url to create url strings for API calls
# Stores the generated URLs in an array of strings
def getApiUrls(num):
    urls = []
    for i in range(0,num):
        urls.append(getRandomIntAndAppend())
    return urls



# Makes the API call and stores films and characters in the FILMS dictionary
def getApiResponses(urls):
    
    for url in urls:
        character_response = requests.get(url)

        if character_response.ok:
            # Loads JSON from response and stores the character's name
            sw_json = json.loads(character_response.content)
            character_name = sw_json['name']
            
            # Iterates over the films this character has been in and adds them to the FILMS dict
            for film_index in range(len(sw_json['films'])):
                film_url = sw_json['films'][film_index]
                film_response = requests.get(film_url)
                film_json = json.loads(film_response.content)
                film_title = film_json['title']
                episode_id = 'episode ' + str(film_json['episode_id'])

                if episode_id not in FILMS:
                    FILMS[episode_id] = {}
                    FILMS[episode_id]['film'] = film_title
                    FILMS[episode_id]['character'] = []
                
                if character_name not in FILMS[episode_id]['character']:
                    FILMS[episode_id]['character'].append(character_name)
        else:
            character_response.raise_for_status()



# Sets up MySQL database connection and creates a new database if not already existing
def setupDatabase(username, password):
    try:
        DB = mysql.connector.connect(
            host='localhost',
            user=username,
            passwd=password,
            database = DB_NAME
        )
        db_cursor = DB.cursor()
        return DB
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
            exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            DB = mysql.connector.connect(
                host='localhost',
                user=username,
                passwd=password
            )
            db_cursor = DB.cursor()
            db_cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
            )
            return DB
            
        else:
            print(err)
            exit(1)


# Creates a table for each film
def createDbTables(DB):
    db_cursor = DB.cursor()

    for episode in FILMS:
        table_name = str(json.dumps(FILMS[episode]['film'])).replace(' ', '_').lower()
        TABLES[episode] = (
            "CREATE TABLE IF NOT EXISTS`" + table_name.strip("\"") + "` ("
            "  `character_name` varchar(255) NOT NULL UNIQUE"
            ") ENGINE=InnoDB"
        )

    for table_name in TABLES:
        db_cursor.execute(TABLES[table_name])



# Inserts character records into film MySQL tables
def insertFilmCharacterRecords(DB):
    db_cursor = DB.cursor()

    # Iterates through characters in FILMS dict and inserts new records into the proper film table
    for episode in FILMS:
        table_name = str(json.dumps(FILMS[episode]['film'])).replace(' ', '_').strip('\"').lower()
        for character_index in range(len(FILMS[episode]['character'])):
            character_name = str(json.dumps(FILMS[episode]['character'][character_index])).replace('\"', '\'')
            sql = "INSERT IGNORE INTO " + table_name + " (character_name) VALUES (" + character_name + ")"
            db_cursor.execute(sql)
            DB.commit()




# Main function controls flow of module
def main():    
    # Takes user input for database username and password and connects to database
    username = input("Please enter username for MySQL connection: ")
    password = getpass.getpass("Please enter the password for the MySQL connection and press return: ")
  
    DB = setupDatabase(username, password)
    
    # Generates URLS for API call
    urls = getApiUrls(15)

    # Passes URLS to getApiResponses() to get JSON
    getApiResponses(urls)

    # Converts the FILMS dict into a JSON object and beautifies to print to console.
    json_formatted = jsbeautifier.beautify(json.dumps(FILMS))
    print(json_formatted)

    try:
        createDbTables(DB)
        insertFilmCharacterRecords(DB)
        print('\n' + 'Database records written successfully!!')
    except mysql.connector.Error as err:
        print(err)
        return



if __name__ == "__main__":
    main()
