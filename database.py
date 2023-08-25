import os
import json
import sqlite3

#other modules
from typing import List, Tuple
from dotenv import load_dotenv

#get data from .env file 
load_dotenv()

##create database
CREATE_PROPERTIES_TABLE = """CREATE TABLE IF NOT EXISTS properties (
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
                                
CREATE_DESCRIPTIONS_TABLE = """CREATE TABLE IF NOT EXISTS descriptions (
                                property_id INTEGER NOT NULL PRIMARY KEY,
                                year_of_construction TEXT,
                                exposition TEXT
                                floor INTEGER,
                                total_floor_number INTEGER,
                                neighborhood_description TEXT,
                                bedroom_number INTEGER
                                toilet_number INTEGER,
                                bathroom_number INTEGER,
                                cellar BOOLEAN,
                                lock_up_garage BOOLEAN,                
                                heating TEXT,
                                tv_cable BOOLEAN,
                                fireplace BOOLEAN,
                                digicode BOOLEAN,
                                intercom BOOLEAN,
                                elevator BOOLEAN,
                                fibre_optics_status TEXT,                   
                                garden BOOLEAN,
                                car_park_number INTEGER,
                                balcony BOOLEAN,
                                large_balcony BOOLEAN,                 
                                estate_agency_fee_percentage INTEGER,
                                pinel BOOLEAN,
                                denormandie BOOLEAN,
                                announce_publication TEXT,
                                announce_last_modification TEXT,                              
                                dpe_date INTEGER,
                                energetic_performance_letter TEXT,
                                energetic_performance_number INTEGER, 
                                climatic_performance_number INTEGER,
                                climatic_performance_letter INTEGER,   
                                estate_agency_id INTEGER,                
                                FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
                                FOREIGN KEY (estate_agency_id) REFERENCES agencies(id)
                            );"""

CREATE_ESTATE_AGENCIES_TABLE = """CREATE TABLE IF NOT EXISTS agencies (
                                id INTEGER NOT NULL PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                fee_percentage INTEGER,
                                evaluation INT
                            );"""

##add data
INSERT_PROPERTY = """INSERT INTO properties (type_of_property, town, district, postcode, url, room_number, 
                    surface, price, date_add_to_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_DESCRIPTION = """INSERT INTO descriptions (property_id, year_of_construction, exposition, floor, total_floor_number, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_AGENCY = """INSERT INTO properties (name, address, fee_percentage, evaluation) VALUES (?, ?, ?, ?);"""

##get data
GET_PROPERTY = "SELECT * FROM properties #####;"
GET_PROPERTY_BY_URL = "SELECT * FROM properties WHERE url = ?;"
GET_ID_URL_FROM_PROPERTIES = "SELECT id, url FROM properties"
GET_PROPERTIES = "SELECT * FROM properties;"
GET_PROPERTIES_FROM_DATE_ADDING_TO_DB = "SELECT * FROM properties WHERE date_add_to_db = ?;"
GET_PROPERTY_DESCRIPTION = "SELECT * FROM descriptions WHERE "
GET_PROPERTY_DESCRIPTION_BY_ID = "SELECT * FROM descriptions WHERE property_id = ?"
GET_AGENCY_ID_BY_NAME = "SELECT id FROM agencies WHERE name = ?;"
GET_AGENCIES = "SELECT * from agencies"


#update data

#delete data

#connection to database
connection = sqlite3.connect(os.environ["DATABASE_PATH"])

def create_table():
    with connection:
        connection.execute(CREATE_PROPERTIES_TABLE)
        connection.execute(CREATE_DESCRIPTIONS_TABLE)
        connection.execute(CREATE_ESTATE_AGENCIES_TABLE)

def add_property(type_of_property: str, town: str, district: str, postcode: int, url: str, room_number: int, surface: int, price: int, date_add_to_db: float):
    with connection:
        connection.execute(INSERT_PROPERTY, (type_of_property, town, district, postcode, url, room_number, surface, price, date_add_to_db))
        
def add_description(property_id, year_of_construction, exposition, floor, total_floor_number, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id):
    with connection:
        connection.execute(INSERT_DESCRIPTION, (property_id, year_of_construction, exposition, floor, total_floor_number, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id))

def add_agency(name: str, address: str, fee_percentage:int, evaluation: int):
    with connection:
        connection.execute(INSERT_AGENCY, (name, address, fee_percentage, evaluation))

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

def get_property_description_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_DESCRIPTION_BY_ID, (id,))
        return cursor.fetchone()

def get_agency(name: str):
    pass

def get_agencies():
    with connection:
        cursor = connection.execute(GET_AGENCIES)
        return cursor.fetchall()
    
def get_agency_id_from_name(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY_ID_BY_NAME, (name,))
        return cursor.fetchall()
    
    