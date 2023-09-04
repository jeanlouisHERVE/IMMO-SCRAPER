import os
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
                                year_of_construction FLOAT,
                                exposition TEXT,
                                floor INTEGER,
                                total_floor_number INTEGER,
                                neighborhood_description LONGTEXT,
                                bedroom_number INTEGER,
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
                                dpe_date TEXT,
                                energetic_performance_letter TEXT,
                                energetic_performance_number INTEGER, 
                                climatic_performance_number INTEGER,
                                climatic_performance_letter TEXT,   
                                estate_agency_id INTEGER,                
                                FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
                                FOREIGN KEY (estate_agency_id) REFERENCES agencies(id)
                            );"""

CREATE_ESTATE_AGENCIES_TABLE = """CREATE TABLE IF NOT EXISTS agencies (
                                id INTEGER NOT NULL PRIMARY KEY,
                                name TEXT UNIQUE,
                                address TEXT,
                                fee_percentage INTEGER,
                                evaluation TEXT
                            );"""

##add data
INSERT_PROPERTY = """INSERT INTO properties (type_of_property, town, district, postcode, url, room_number, 
                    surface, price, date_add_to_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_DESCRIPTION = """INSERT INTO descriptions (property_id, year_of_construction, exposition, floor, total_floor_number, neighborhood_description, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_AGENCY = """INSERT INTO agencies (name, address, fee_percentage, evaluation) VALUES (?, ?, ?, ?);"""

##get data
GET_PROPERTY = "SELECT * FROM properties #####;"
GET_PROPERTY_BY_URL = "SELECT * FROM properties WHERE url = ?;"
GET_PROPERTY_BY_ID = "SELECT * FROM properties WHERE id = ?;"
GET_ID_URL_FROM_PROPERTIES = "SELECT id, url FROM properties"
GET_ID_URL_DATEOFMODIFICATION_FROM_PROPERTIES = "SELECT p.id, p.url, d.announce_last_modification FROM properties p JOIN descriptions d ON p.id = d.property_id;"
GET_PROPERTIES = "SELECT * FROM properties;"
GET_PROPERTIES_NUMBER = "SELECT COUNT(id) FROM properties;"
GET_PROPERTIES_FROM_DATE_ADDING_TO_DB = "SELECT * FROM properties WHERE date_add_to_db = ?;"
GET_PROPERTY_DESCRIPTION = "SELECT * FROM descriptions WHERE "
GET_PROPERTY_DESCRIPTION_BY_ID = "SELECT * FROM descriptions WHERE property_id = ?"
GET_AGENCY_ID_BY_NAME = "SELECT id FROM agencies WHERE name = ?;"
GET_AGENCIES = "SELECT * from agencies"
GET_AGENCY = "SELECT * from agencies WHERE name = ?"

#update data
UPDATE_PROPERTY = """UPDATE properties
                    SET price = ?
                    WHERE id = ?;"""
UPDATE_DESCRIPTION = """UPDATE descriptions
                    SET year_of_construction = ?, exposition = ?, floor = ?, total_floor_number = ?,
                        neighborhood_description = ?, bedroom_number = ?, toilet_number = ?, bathroom_number = ?, cellar = ?,
                        lock_up_garage = ?, heating = ?, tv_cable = ?, fireplace = ?, digicode = ?, intercom = ?,
                        elevator = ?, fibre_optics_status = ?, garden = ?, car_park_number = ?, balcony = ?,
                        large_balcony = ?, estate_agency_fee_percentage = ?, pinel = ?, denormandie = ?,
                        announce_publication = ?, announce_last_modification = ?, dpe_date = ?,
                        energetic_performance_letter = ?, energetic_performance_number = ?, climatic_performance_number = ?,
                        climatic_performance_letter = ?, estate_agency_id = ?
                    WHERE property_id = ?;"""
UPDATE_AGENCY = """UPDATE agencies
                    SET name = ?, address = ?, fee_percentage = ?, evaluation = ?
                    WHERE agency_id = ?;"""

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
        
def add_description(property_id: int, year_of_construction: float, exposition: str, floor: int, total_floor_number: int, neighborhood_description: str, bedroom_number: int, toilet_number: int, bathroom_number: int, cellar: bool, lock_up_garage: bool, heating: bool, tv_cable: bool, fireplace: bool, digicode: bool, intercom: bool, elevator: bool, fibre_optics_status: str, garden: bool, car_park_number: int, balcony: bool, large_balcony: bool,  estate_agency_fee_percentage: float, pinel: bool, denormandie: bool, announce_publication: str, announce_last_modification: str, dpe_date: str, energetic_performance_letter: str, energetic_performance_number: int, climatic_performance_number: int, climatic_performance_letter: str, estate_agency_id: int):
    with connection:
        connection.execute(INSERT_DESCRIPTION, (property_id, year_of_construction, exposition, floor, total_floor_number, neighborhood_description, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id))

def add_agency(name: str, address: str, fee_percentage:int, evaluation: str):
    with connection:
        connection.execute(INSERT_AGENCY, (name, address, fee_percentage, evaluation))

def get_property_by_url(url: str):
    with connection:
        cursor = connection.execute(GET_PROPERTY_BY_URL, (url,))
        return cursor.fetchone()

def get_property_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_BY_ID, (id,))
        return cursor.fetchone()

def get_id_url_from_properties():
    with connection:
        cursor = connection.execute(GET_ID_URL_FROM_PROPERTIES)
        return cursor.fetchall()
    
def get_id_url_dateofmodification_from_properties():
    with connection:
        cursor = connection.execute(GET_ID_URL_DATEOFMODIFICATION_FROM_PROPERTIES)
        return cursor.fetchall()
    
def get_properties():
    with connection:
        cursor = connection.execute(GET_PROPERTIES)
        return cursor.fetchall()

def get_properties_number():
    with connection:
        cursor = connection.execute(GET_PROPERTIES_NUMBER)
        return cursor.fetchall()

def get_properties_from_adding_date(date_add_to_db: float):
    with connection:
        cursor = connection.execute(GET_PROPERTIES_FROM_DATE_ADDING_TO_DB, (date_add_to_db, ))
        return cursor.fetchall()

def get_property_description_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_DESCRIPTION_BY_ID, (id,))
        return cursor.fetchone()

def get_agency(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY, (name,))
        return cursor.fetchone()

def get_agencies():
    with connection:
        cursor = connection.execute(GET_AGENCIES)
        return cursor.fetchall()
    
def get_agency_id_from_name(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY_ID_BY_NAME, (name,))
        return cursor.fetchall()
    
def update_property(id: int, price: int):
    try:
        with connection:
            connection.execute(UPDATE_PROPERTY, (price, id))
        print(f"OK : Property {id} updated successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error updating property {id}: {e}")

def update_description(property_id: int, year_of_construction: float, exposition: str, floor: int, total_floor_number: int, neighborhood_description: str, bedroom_number: int, toilet_number: int, bathroom_number: int, cellar: bool, lock_up_garage: bool, heating: bool, tv_cable: bool, fireplace: bool, digicode: bool, intercom: bool, elevator: bool, fibre_optics_status: str, garden: bool, car_park_number: int, balcony: bool, large_balcony: bool,  estate_agency_fee_percentage: float, pinel: bool, denormandie: bool, announce_publication: str, announce_last_modification: str, dpe_date: str, energetic_performance_letter: str, energetic_performance_number: int, climatic_performance_number: int, climatic_performance_letter: str, estate_agency_id: int):
    try:
        with connection:
            connection.execute(UPDATE_DESCRIPTION, (year_of_construction, exposition, floor, total_floor_number, neighborhood_description, bedroom_number, toilet_number, bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode, intercom, elevator, fibre_optics_status, garden, car_park_number, balcony, large_balcony, estate_agency_fee_percentage, pinel, denormandie, announce_publication, announce_last_modification, dpe_date, energetic_performance_letter, energetic_performance_number, climatic_performance_number, climatic_performance_letter, estate_agency_id, property_id))
        print(f"OK : Description for Property {property_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error updating description for Property {property_id}: {e}")
        
def update_agency(name: str, address: str, fee_percentage:int, evaluation: str):
    try:
        with connection:
            connection.execute(UPDATE_AGENCY, (name, address, fee_percentage, evaluation))
        print(f"OK : Agency {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error updating agency {name}: {e}")
