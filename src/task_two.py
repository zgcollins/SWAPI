# This script pulls data for Star Wars Episode 4: A New Hope from the Star Wars films API
# The script will replace the retreived URL endpoints corresponding to the characters, starships,
# vehicles, and species associated with that film with the actual data retrieved from the endpoints

# Flow of control maintained in the main() function

# Import 'json' and 'requests' to make API calls
# Import 'jsbeautifier' for pretty printing JSON
# Import 're' for regex checking of strings
import json
import requests
import jsbeautifier
import re

# Base URL for A New Hope
BASE_URL = 'https://swapi.co/api/films/1'


# Dictionary to store replacement episode data
EPISODE_FOUR = {
    'title': '',
    'episode_id': 4,
    'opening_crawl': '',
    'director': '',
    'producer': '',
    'release_date': '',
    'characters': [],
    'planets': [],
    'starships': [],
    'vehicles': [],
    'species': [],
    'created': '',
    'edited': '',
    'url': BASE_URL
}




# Gets the film JSON data from the API endpoint
def getApiData(url):
    response = requests.get(url)

    if response.ok:
        data = json.loads(response.content)
        return data
    else:
        response.raise_for_status()
        print('Problem with ' + url)


# Populates empty fields in EPISODE_FOUR dict with film's JSON data
def populateFilmDict(film_json):
    for key in film_json:
        if key not in ('characters', 'planets', 'starships', 'vehicles', 'species'):
            EPISODE_FOUR[key] = film_json[key]
            




# Retreieves endpoints from the json parameter and adds data to the EPISODE_FOUR dict   
def processFilmJson(data):
    
    # Iterate through nested URLS
    # For each URL, retrieve the data from the API endpoint
    # For each key in the retrieved API data, append values to the appropriate nested dict in EPISODE_FOUR dict 
    for key in ('characters', 'planets', 'starships', 'vehicles', 'species'):
        for url in data[key]:
            api_data = getApiData(url)                 
            EPISODE_FOUR[key].append(api_data)
    
        




# Converts all the characters' measurements from metric to standard
def convertMetricToStandard(characters):
    CONVERSIONS = {'cm_to_in': 2.54, 'kg_to_lb': 2.205}
    
    for character in characters:
        if character['height'] != 'unknown':
            character_height_cm = int(re.sub('[^0-9]', '', character['height']))
            character['height'] = character_height_cm / CONVERSIONS['cm_to_in']
            character['height'] = str(character['height'])

        if character['mass'] != 'unknown':
            character_weight_kg = int(re.sub('[^0-9]', '', character['mass']))
            character['mass'] = character_weight_kg * CONVERSIONS['kg_to_lb']
            character['mass'] = str(character['mass'])


# Removes nested URLS from a list of dictionaries and returns the list
def removeNestedUrlsFromList(nested_list):
    for index in range(len(nested_list)):
        try:
            nested_list[index] = {k: v for k, v in nested_list[index].items() if not isinstance(v, list) and str(k) != "url"}
            for key in nested_list[index]:
                if key == "homeworld" and nested_list[index][key].startswith("http"):
                    homeworld_api_data = getApiData(nested_list[index][key])
                    nested_list[index][key] = homeworld_api_data['name']
        except AttributeError:
            continue
    return nested_list




# Controls the flow of the module
def main():
    # Gets the film JSON from the endpoint
    film_json = getApiData(BASE_URL)

    # Populates EPISODE_FOUR dictionary with JSON data
    populateFilmDict(film_json)

    # Goes through the film_json to retreieve character, planet, starship, vehicle, and species data
    # and add to the EPISODE_FOUR dict
    processFilmJson(film_json)

    # Finally, convert all of the characters' measurements from metric to standard
    convertMetricToStandard(EPISODE_FOUR['characters'])

    # Remove cross references
    for key in EPISODE_FOUR:
        if key in ('characters', 'planets', 'starships', 'vehicles', 'species'):
            nested_list = EPISODE_FOUR[key]
            EPISODE_FOUR[key] = removeNestedUrlsFromList(nested_list)
    



    # Write to JSON file
    with open('task_two.json', 'w') as outfile:
        json.dump(EPISODE_FOUR, outfile, indent=4)
    





if __name__ == "__main__":
    main()