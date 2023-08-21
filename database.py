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
                                district TEXT,
                                postcode TEXT,                               
                                url TEXT,
                                room_number INTEGER,
                                surface INTEGER, 
                                price INTEGER,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
                                
CREATE_DESCRIPTION_TABLE = """CREATE TABLE IF NOT EXISTS descriptions (
                                property_id INTEGER NOT NULL PRIMARY KEY,
                                exposition TEXT,
                                bathroom_number INTEGER,
                                heating TEXT,
                                garden BOOLEAN,
                                toilet_number INTEGER,
                                car_park_number INTEGER,
                                year_of_construction TEXT,
                                dpe_date TIMESTAMP,
                                energetic_performance_letter TEXT,
                                energetic_performance_number INTEGER,
                                climatic_performance_letter TEXT, 
                                climatic_performance_number INTEGER,
                                announce_publication TIMESTAMP,
                                announce_last_modification TIMESTAMP,
                                neighborhood_description LONGTEXT,
                                floor INT,
                                estate_agency_id, 
                                FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
                                FOREIGN KEY (estate_agency_id) REFERENCES agencies(id)
                            );"""

CREATE_ESTATE_AGENCY_TABLE = """CREATE TABLE IF NOT EXISTS agencies (
                                id INTEGER NOT NULL PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                evaluation INT
                            );"""

##add data
INSERT_PROPERTY = """INSERT INTO properties (type_of_property, town, district, postcode, url, room_number, 
                    surface, price, date_add_to_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_DESCRIPTION = """INSERT INTO description (exposition, bathroom_number, heating, garden, toilet_number, 
                    car_park_number, year_of_construction, dpe_date, energetic_performance_letter, energetic_performance_letter, climatic_performance_letter,
                    climatic_performance_letter, announce_publication, announce_last_modification, neighborhood_description, floor, estate_agency_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_AGENCY = """INSERT INTO properties (name, address, evaluation) VALUES (?, ?, ?);"""

##get data
GET_PROPERTY = "SELECT * FROM properties #####;"
GET_PROPERTY_BY_URL = "SELECT * FROM properties WHERE url = ?;"
GET_ID_URL_FROM_PROPERTIES = "SELECT id, url FROM properties"
GET_PROPERTIES = "SELECT * FROM properties;"
GET_PROPERTIES_FROM_DATE_ADDING_TO_DB = "SELECT * FROM properties WHERE date_add_to_db = ?;"
GET_PROPERTY_DESCRIPTION = "SELECT * FROM description WHERE "
GET_AGENCY_BY_NAME = "SELECT agency_id FROM agencies WHERE name = ?;"
GET_AGENCIES = "SELECT * from agencies"

#update data

#delete data

#connection to database
connection = sqlite3.connect(os.environ["DATABASE_PATH"])

def create_table():
    with connection:
        connection.execute(CREATE_PROPERTY_TABLE)
        #connection.execute(CREATE_DESCRIPTION_TABLE)
        connection.execute(CREATE_ESTATE_AGENCY_TABLE)

def add_property(type_of_property: str, town: str, district: str, postcode: int, url: str, room_number: int, surface: int, price: int, date_add_to_db: float):
    with connection:
        connection.execute(INSERT_PROPERTY, (type_of_property, town, district, postcode, url, room_number, surface, price, date_add_to_db))
        
def add_description(exposition: str, bathroom_number: int, heating: str, garden: bool, toilet_number: int, car_park_number: int, year_of_construction: str, dpe_date: float, energetic_performance_letter: str, energetic_performance_number: int, climatic_performance_letter: str,
                    climatic_performance_number: int, announce_publication: float, announce_last_modification: float, neighborhood_description: str, floor: int, estate_agency_id: int):
    with connection:
        connection.execute(INSERT_DESCRIPTION, (exposition, bathroom_number, heating, garden, toilet_number, car_park_number, year_of_construction, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_letter,
                    climatic_performance_number, announce_publication, announce_last_modification, neighborhood_description, floor, estate_agency_id))

def add_agency(name: str, address: str, evaluation: int):
    with connection:
        connection.execute(INSERT_PROPERTY, (name, address, evaluation))

def get_property_by_url(url: str):
    with connection:
        cursor = connection.execute(GET_PROPERTY_BY_URL, (url,))
        return cursor.fetchone()

def get_id_url_from_properties():
    with connection:
        cursor = connection.execute(GET_ID_URL_FROM_PROPERTIES)
        return cursor.fetchall()
    
def get_properties():
    with connection:
        #connection.execute(INSERT_DESCRIPTION, ())
        pass

def get_properties_from_adding_date(date_add_to_db: float):
    with connection:
        cursor = connection.execute(GET_PROPERTIES_FROM_DATE_ADDING_TO_DB, (date_add_to_db, ))
        return cursor.fetchall()

def get_agency(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY_BY_NAME, (name, ))
        return cursor.fetchone()

def get_agencies():
    with connection:
        cursor = connection.execute(GET_AGENCIES)
        return cursor.fetchall()