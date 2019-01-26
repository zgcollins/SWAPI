# mySWAPI Fun Times

This is Zack Collins's implementation of the SWAPI tasks given by Red Hat for technical assessment of programming skills.

* The project consists of two scripts...
	* task_one.py
		* When run, this task will generate 15 random integers between 1 and 87 (not including 17, which returns a 404 error from the API endpoint)
		* The 15 random integers will correspond to character IDs in the Star Wars people API
		* Each of the 15 SW character's data will be retreived from the API, stored in a Python dictionary, and written to a MySQL database. See below for a description of DB schema.
		* The script will then write a beautified JSON object to the console. The JSON object will have dictionary keys corresponding to each film's episode number, and a nested dictionary with the film's title and all the characters that appeared in each film. The JSON data printed to console will only include the 15 characters that were queried initially. However the MySQL database will aggregate more and more character records as the task is run. 
	* task_two.py
		* When run, the task will retrieve data for SW Episode 4: A New Hope
		* The film data will be stored in a dictionary. All of the referenced URLs for the film's data will be queried and the URLs will be replaced with the actual data.
		* The character height and mass will be converted from metric to standard.
		* The newly created dictionary will be written to a JSON file called task_two.json
		* The new dictionary will not contain any cross-referenced URLs


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need the following to run... 
* Python 3.* or later
* A MySQL instance on your local machine and the credentials to log into the server
* The following libraries/modules (use pip install from cmd line if any are missing)
	* json
	* random
	* getpass
	* jsbeautifier
	* requests
	* mysql-connector


### Installing

You will call each of the two tasks directly from the command line to run these programs.
Import the project to a directory on your local machine. Open the command line and navigate to said directory to run.


### Running the Program

Once you are in the project's src directory, run task_one.py from the console. You will be prompted for your MySQL server credentials. The script will take care of the rest. You can use a MySQL IDE such as MySQL Workbench to query the database tables and observe the newly created records. See below for more database details.

Similarly, run task_two.py from the command line to execute the script. The resulting JSON file will be written to your working directory.


## Database

For task_one.py, the MySQL database will consist of a table for each of the films that appears in the character query (i.e. if no character from a particular film is queried, that film's table will not appear in the database). Each table simply has a column for character_name, which is unique.

task_one.py can be run multiple times to continue populating the database with character records. For subsequent runs of task_one.py, any duplicate character records in a given film's table will not be overwritten or replaced. They will simply be ignored. With enough iterations, task_one.py will populate the MySQL database with all of the characters in the SW universe (except person number 17, of course :no_entry_sign: ).

## References

* MySQL Connector/Python Developer Guide
	* https://dev.mysql.com/doc/connector-python/en/
	* This was a necessary guide for the developer that normally relies too heavily on Django to manage SQL transactions :no_mouth:

## Additional Notes
