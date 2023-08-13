import os
import json
import sqlite3

#other modules
from typing import List, Tuple
from dotenv import load_dotenv

#get data from .env file 
load_dotenv()

##create database
CREATE_PROPERTY_TABLE = """CREATE TABLE IF NOT EXISTS properties (
                                id INTEGER NOT NULL PRIMARY KEY, 
                                type_of_property TEXT, 
                                town TEXT,
                                postcode TEXT,
                                district TEXT,
                                link TEXT
                                url TEXT,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
CREATE_DESCRIPTION_TABLE = """CREATE TABLE IF NOT EXISTS descriptions (
                                FOREIGN KEY (pseudo) REFERENCES properties(pseudo) ON DELETE CASCADE
                            );"""

##add data
INSERT_PROPERTY = "INSERT INTO  () VALUES ();"
INSERT_DESCRIPTION = """INSERT INTO description () VALUES ()"""

##get data
GET_PROPERTY = "SELECT * FROM camgirls #####;"
GET_PROPERTY_DESCRIPTION = "SELECT pseudo FROM description #####"
GET_PROPERTIES = "SELECT * FROM properties;"

#update data

#delete data

#connection to database
connection = sqlite3.connect(os.environ["DATABASE_PATH"])

def create_table():
    with connection:
        connection.execute(CREATE_PROPERTY_TABLE)
        #connection.execute(CREATE_DESCRIPTION_TABLE)

def add_property():
    with connection:
        # connection.execute(INSERT_PROPERTY, ())
        pass
        
def add_description():
    with connection:
        #connection.execute(INSERT_DESCRIPTION, ())
        pass

def get_property():
    with connection:
        #connection.execute(INSERT_DESCRIPTION, ())
        pass
    
def get_properties():
    with connection:
        #connection.execute(INSERT_DESCRIPTION, ())
        pass