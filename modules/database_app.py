import sqlite3
# import platform

# other modules

from dotenv import load_dotenv

# get data from .env file
load_dotenv()

# variables
WINDOWS_DATABASE_PATH = "c:\\Users\\jeanl\\OneDrive\\Bureau\\IMMO-SCRAPER\\database\\immoscraper.db"
LINUX_DATABASE_PATH = "/home/jean-louis/Bureau/IMMO-SCRAPER/database/immoscraper.db"

# # Distinguishing between different operating systems:
# if platform.system() == "Linux":
#     connection = sqlite3.connect(LINUX_DATABASE_PATH)
# elif platform.system() == "Windows":
#     connection = sqlite3.connect(WINDOWS_DATABASE_PATH)
# else:
#     print("OS not compatible")

connection = sqlite3.connect(WINDOWS_DATABASE_PATH)

# create database
CREATE_PROPERTIES_TABLE = """CREATE TABLE IF NOT EXISTS properties (
                                id INTEGER NOT NULL PRIMARY KEY,
                                type_of_property TEXT,
                                town TEXT,
                                district TEXT,
                                postcode TEXT,
                                url TEXT,
                                room_number INTEGER,
                                surface INTEGER,
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
                                announce_publication TIMESTAMP,
                                announce_last_modification TIMESTAMP,
                                dpe_date TIMESTAMP,
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
                                evaluation TEXT,
                                total_announces INTEGER DEFAULT 1,
                                total_announces_active INTEGER DEFAULT 1
                            );"""

CREATE_PRICES_TABLE = """CREATE TABLE IF NOT EXISTS prices (
                        id INTEGER NOT NULL PRIMARY KEY,
                        date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        property_id INTEGER NOT NULL,
                        price REAL,
                        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
                    );"""

CREATE_OLD_PROPERTIES_TABLE = """CREATE TABLE IF NOT EXISTS old_properties (
                                id INTEGER NOT NULL PRIMARY KEY,
                                type_of_property TEXT,
                                town TEXT,
                                district TEXT,
                                postcode TEXT,
                                url TEXT,
                                room_number INTEGER,
                                surface INTEGER,
                                date_add_to_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""

CREATE_OLD_DESCRIPTIONS_TABLE = """CREATE TABLE IF NOT EXISTS old_descriptions (
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
                                announce_publication TIMESTAMP,
                                announce_last_modification TIMESTAMP,
                                dpe_date TIMESTAMP,
                                energetic_performance_letter TEXT,
                                energetic_performance_number INTEGER,
                                climatic_performance_number INTEGER,
                                climatic_performance_letter TEXT,
                                estate_agency_id INTEGER,
                                FOREIGN KEY (property_id) REFERENCES old_properties(id) ON DELETE CASCADE,
                                FOREIGN KEY (estate_agency_id) REFERENCES agencies(id)
                            );"""
CREATE_OLD_PRICES_TABLE = """CREATE TABLE IF NOT EXISTS old_prices (
                            id INTEGER NOT NULL PRIMARY KEY,
                            date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                            property_id INTEGER NOT NULL,
                            price REAL,
                            FOREIGN KEY (property_id) REFERENCES old_properties(id) ON DELETE CASCADE
                        );"""

# add data
INSERT_PROPERTY = """INSERT INTO properties (type_of_property, town, district, postcode, url, room_number,
                    surface, date_add_to_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_DESCRIPTION = """INSERT INTO descriptions (property_id, year_of_construction, exposition, floor,
                    total_floor_number, neighborhood_description, bedroom_number, toilet_number,
                    bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode,
                    intercom, elevator, fibre_optics_status, garden, car_park_number, balcony,
                    large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication,
                    announce_last_modification, dpe_date, energetic_performance_letter,
                    energetic_performance_number, climatic_performance_number, climatic_performance_letter,
                    estate_agency_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_AGENCY = """INSERT INTO agencies (name,
                                         address,
                                         fee_percentage,
                                         evaluation,
                                         total_announces,
                                         total_announces_active)
                        VALUES (?, ?, ?, ?, ?, ?);"""
INSERT_PRICE = """INSERT INTO prices (date, property_id, price) VALUES (?, ?, ?);"""
INSERT_OLD_PROPERTY = """INSERT INTO old_properties (type_of_property, town, district, postcode, url,
                    room_number, surface, date_add_to_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_OLD_DESCRIPTION = """INSERT INTO old_descriptions (property_id, year_of_construction, exposition,
                    floor, total_floor_number, neighborhood_description, bedroom_number, toilet_number,
                    bathroom_number, cellar, lock_up_garage, heating, tv_cable, fireplace, digicode,
                    intercom, elevator, fibre_optics_status, garden, car_park_number, balcony,
                    large_balcony,  estate_agency_fee_percentage, pinel, denormandie, announce_publication,
                    announce_last_modification, dpe_date, energetic_performance_letter,
                    energetic_performance_number, climatic_performance_number, climatic_performance_letter,
                    estate_agency_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
INSERT_OLD_PRICE = """INSERT INTO old_prices (date, property_id, price) VALUES (?, ?, ?);"""

# get data
GET_PROPERTY = "SELECT * FROM properties #####;"
GET_PROPERTY_BY_URL = "SELECT * FROM properties WHERE url = ?;"
GET_PROPERTY_BY_ID = "SELECT * FROM properties WHERE id = ?;"
GET_OLD_PROPERTY_BY_ID = "SELECT * FROM old_properties WHERE id = ?;"
GET_PROPERTY_PRICES = "SELECT * FROM prices WHERE property_id = ?;"
GET_ID_URL_FROM_PROPERTIES = "SELECT id, url FROM properties"
GET_ID_URL_DATEOFMODIFICATION_FROM_PROPERTIES = """
                                        SELECT p.id, p.url, d.announce_last_modification FROM properties
                                        p JOIN descriptions d ON p.id = d.property_id
                                        ORDER BY RANDOM()
                                        ;"""
GET_PROPERTIES = "SELECT * FROM properties;"
GET_PROPERTIES_NUMBER = "SELECT COUNT(id) FROM properties;"
GET_PROPERTIES_FROM_DATE_ADDING_TO_DB = "SELECT * FROM properties WHERE date_add_to_db = ?;"
GET_PROPERTIES_DESCRIPTIONS = "SELECT * FROM descriptions"
GET_PROPERTY_DESCRIPTION_BY_ID = "SELECT * FROM descriptions WHERE property_id = ?"
GET_OLD_PROPERTIES = "SELECT * FROM old_properties;"
GET_OLD_PROPERTIES_DESCRIPTIONS = "SELECT * FROM old_descriptions"
GET_OLD_PROPERTY_DESCRIPTION_BY_ID = "SELECT * FROM descriptions WHERE property_id = ?"
GET_AGENCY_ID_BY_NAME = "SELECT id FROM agencies WHERE name = ?;"
GET_AGENCIES = "SELECT * FROM agencies"
GET_AGENCY_BY_NAME = "SELECT * FROM agencies WHERE name = ?"
GET_PRICES = "SELECT * FROM prices"
GET_PRICES_BY_PROPERTY_ID = "SELECT * FROM prices WHERE property_id = ?;"
GET_LAST_PRICE_FOR_PROPRIETY = """SELECT price FROM prices
                                WHERE property_id = ? ORDER BY date DESC LIMIT 1"""
GET_OLD_PRICES = "SELECT * FROM old_prices"

# update data
UPDATE_PROPERTY = """UPDATE properties
                    SET price = ?
                    WHERE id = ?;"""
UPDATE_DESCRIPTION = """UPDATE descriptions
                       SET year_of_construction = ?,
                           exposition = ?,
                           floor = ?,
                           total_floor_number = ?,
                           neighborhood_description = ?,
                           bedroom_number = ?,
                           toilet_number = ?,
                           bathroom_number = ?,
                           cellar = ?,
                           lock_up_garage = ?,
                           heating = ?,
                           tv_cable = ?,
                           fireplace = ?,
                           digicode = ?,
                           intercom = ?,
                           elevator = ?,
                           fibre_optics_status = ?,
                           garden = ?,
                           car_park_number = ?,
                           balcony = ?,
                           large_balcony = ?,
                           estate_agency_fee_percentage = ?,
                           pinel = ?,
                           denormandie = ?,
                           announce_publication = ?,
                           announce_last_modification = ?,
                           dpe_date = ?,
                           energetic_performance_letter = ?,
                           energetic_performance_number = ?,
                           climatic_performance_number = ?,
                           climatic_performance_letter = ?,
                           estate_agency_id = ?
                       WHERE property_id = ?;"""
UPDATE_AGENCY = """UPDATE agencies
                    SET name = ?,
                    address = ?,
                    fee_percentage = ?,
                    evaluation = ?,
                    total_announces = ?,
                    total_announces_active = ?
                    WHERE id = ?;"""
UPDATE_AGENCY_TOTALS = """UPDATE agencies
                            SET total_announces_active = total_announces_active + 1,
                            total_announces = total_announces + 1
                            WHERE id = ?", (agency_id,)"""
UPDATE_AGENCY_TOTAL_ACTIVE_DECREMENT = """UPDATE agencies
                                            SET total_announces_active = total_announces_active - 1
                                            WHERE id = ?"""

# delete data
DELETE_PROPERTIES_TABLE = "DELETE FROM properties;"
DELETE_PRICES_TABLE = "DELETE FROM prices;"
DELETE_DESCRIPTIONS_TABLE = "DELETE FROM descriptions;"
DELETE_AGENCIES_TABLE = "DELETE FROM agencies;"
DELETE_OLD_PROPERTIES_TABLE = "DELETE FROM old_properties;"
DELETE_OLD_PRICES_TABLE = "DELETE FROM old_prices;"
DELETE_OLD_DESCRIPTIONS_TABLE = "DELETE FROM old_descriptions;"
DELETE_PROPERTY = "DELETE FROM properties WHERE id = ?;"


def create_tables():
    with connection:
        print("Creating tables...")
        connection.execute(CREATE_PROPERTIES_TABLE)
        connection.execute(CREATE_OLD_PROPERTIES_TABLE)
        connection.execute(CREATE_PRICES_TABLE)
        connection.execute(CREATE_OLD_PRICES_TABLE)
        connection.execute(CREATE_DESCRIPTIONS_TABLE)
        connection.execute(CREATE_OLD_DESCRIPTIONS_TABLE)
        connection.execute(CREATE_ESTATE_AGENCIES_TABLE)
        print("Tables created.")


def delete_tables():
    with connection:
        print("deleting tables...")
        connection.execute(DELETE_PROPERTIES_TABLE)
        connection.execute(DELETE_OLD_PROPERTIES_TABLE)
        connection.execute(DELETE_PRICES_TABLE)
        connection.execute(DELETE_OLD_PRICES_TABLE)
        connection.execute(DELETE_DESCRIPTIONS_TABLE)
        connection.execute(DELETE_OLD_DESCRIPTIONS_TABLE)
        connection.execute(DELETE_AGENCIES_TABLE)
        print("Tables deleted.")


def add_property(
        type_of_property: str,
        town: str,
        district: str,
        postcode: int,
        url: str,
        room_number: int,
        surface: int,
        date_add_to_db: float):
    with connection:
        cursor = connection.execute(INSERT_PROPERTY, (
                                                        type_of_property,
                                                        town,
                                                        district,
                                                        postcode,
                                                        url,
                                                        room_number,
                                                        surface,
                                                        date_add_to_db)
                                    )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_old_property(
        type_of_property: str,
        town: str,
        district: str,
        postcode: int,
        url: str,
        room_number: int,
        surface: int,
        date_add_to_db: float):
    with connection:
        cursor = connection.execute(INSERT_OLD_PROPERTY, (
                                                            type_of_property,
                                                            town,
                                                            district,
                                                            postcode,
                                                            url,
                                                            room_number,
                                                            surface,
                                                            date_add_to_db)
                                    )
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_description(
        property_id: int,
        year_of_construction: float,
        exposition: str,
        floor: int,
        total_floor_number: int,
        neighborhood_description: str,
        bedroom_number: int,
        toilet_number: int,
        bathroom_number: int,
        cellar: bool,
        lock_up_garage: bool,
        heating: bool,
        tv_cable: bool,
        fireplace: bool,
        digicode: bool,
        intercom: bool,
        elevator: bool,
        fibre_optics_status: str,
        garden: bool,
        car_park_number: int,
        balcony: bool,
        large_balcony: bool,
        estate_agency_fee_percentage: float,
        pinel: bool,
        denormandie: bool,
        announce_publication: float,
        announce_last_modification: float,
        dpe_date: float,
        energetic_performance_letter: str,
        energetic_performance_number: int,
        climatic_performance_number: int,
        climatic_performance_letter: str,
        estate_agency_id: int):
    try:
        with connection:
            connection.execute(INSERT_DESCRIPTION, (property_id,
                                                    year_of_construction,
                                                    exposition, floor,
                                                    total_floor_number,
                                                    neighborhood_description,
                                                    bedroom_number,
                                                    toilet_number,
                                                    bathroom_number,
                                                    cellar,
                                                    lock_up_garage,
                                                    heating,
                                                    tv_cable,
                                                    fireplace,
                                                    digicode,
                                                    intercom,
                                                    elevator,
                                                    fibre_optics_status,
                                                    garden,
                                                    car_park_number,
                                                    balcony,
                                                    large_balcony,
                                                    estate_agency_fee_percentage,
                                                    pinel,
                                                    denormandie,
                                                    announce_publication,
                                                    announce_last_modification,
                                                    dpe_date,
                                                    energetic_performance_letter,
                                                    energetic_performance_number,
                                                    climatic_performance_number,
                                                    climatic_performance_letter,
                                                    estate_agency_id)
                               )
        print(f"OK : Property {property_id} 's description has been saved successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error saving property {property_id} description: {e}")


def add_old_description(
        property_id: int,
        year_of_construction: float,
        exposition: str,
        floor: int,
        total_floor_number: int,
        neighborhood_description: str,
        bedroom_number: int,
        toilet_number: int,
        bathroom_number: int,
        cellar: bool,
        lock_up_garage: bool,
        heating: bool,
        tv_cable: bool,
        fireplace: bool,
        digicode: bool,
        intercom: bool,
        elevator: bool,
        fibre_optics_status: str,
        garden: bool,
        car_park_number: int,
        balcony: bool,
        large_balcony: bool,
        estate_agency_fee_percentage: float,
        pinel: bool,
        denormandie: bool,
        announce_publication: float,
        announce_last_modification: float,
        dpe_date: float,
        energetic_performance_letter: str,
        energetic_performance_number: int,
        climatic_performance_number: int,
        climatic_performance_letter: str,
        estate_agency_id: int):
    with connection:
        connection.execute(INSERT_OLD_DESCRIPTION, (property_id,
                                                    year_of_construction,
                                                    exposition, floor,
                                                    total_floor_number,
                                                    neighborhood_description,
                                                    bedroom_number,
                                                    toilet_number,
                                                    bathroom_number,
                                                    cellar,
                                                    lock_up_garage,
                                                    heating,
                                                    tv_cable,
                                                    fireplace,
                                                    digicode,
                                                    intercom,
                                                    elevator,
                                                    fibre_optics_status,
                                                    garden,
                                                    car_park_number,
                                                    balcony,
                                                    large_balcony,
                                                    estate_agency_fee_percentage,
                                                    pinel,
                                                    denormandie,
                                                    announce_publication,
                                                    announce_last_modification,
                                                    dpe_date,
                                                    energetic_performance_letter,
                                                    energetic_performance_number,
                                                    climatic_performance_number,
                                                    climatic_performance_letter,
                                                    estate_agency_id)
                           )


def add_agency(name: str,
               address: str,
               fee_percentage: int,
               evaluation: str,
               total_announces: int,
               total_announces_active: int):
    with connection:
        cursor = connection.execute(INSERT_AGENCY, (name,
                                                    address,
                                                    fee_percentage,
                                                    evaluation,
                                                    total_announces,
                                                    total_announces_active))
        last_inserted_id = cursor.lastrowid
    return last_inserted_id


def add_price_to_property(date: float, property_id: int, price: int):
    with connection:
        connection.execute(INSERT_PRICE, (date, property_id, price))


def add_old_price_to_old_property(date: float, property_id: int, price: int):
    with connection:
        connection.execute(INSERT_OLD_PRICE, (date, property_id, price))


def get_property_by_url(url: str):
    with connection:
        cursor = connection.execute(GET_PROPERTY_BY_URL, (url,))
        return cursor.fetchone()


def get_property_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_BY_ID, (id,))
        return cursor.fetchone()


def get_old_property_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_OLD_PROPERTY_BY_ID, (id,))
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


def get_property_prices(property_id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_PRICES, (property_id,))
        return cursor.fetchone()


def get_last_price_for_property(property_id: int):
    with connection:
        cursor = connection.cursor()
        cursor.execute(GET_LAST_PRICE_FOR_PROPRIETY, (property_id,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None  # Property not found or no prices registere


def get_properties_descriptions():
    with connection:
        cursor = connection.execute(GET_PROPERTIES_DESCRIPTIONS)
        return cursor.fetchall()


def get_property_description_by_id(id: int):
    with connection:
        cursor = connection.execute(GET_PROPERTY_DESCRIPTION_BY_ID, (id,))
        return cursor.fetchone()


def get_estate_agency_id_by_property_id(property_id: int):
    result = connection.execute(GET_PROPERTY_DESCRIPTION_BY_ID, (property_id,)).fetchone()
    if result:
        estate_agency_id = result["estate_agency_id"]
        return estate_agency_id
    else:
        return None


def get_old_properties():
    with connection:
        cursor = connection.execute(GET_OLD_PROPERTIES)
        return cursor.fetchall()


def get_old_properties_descriptions():
    with connection:
        cursor = connection.execute(GET_OLD_PROPERTIES_DESCRIPTIONS)
        return cursor.fetchall()


def get_agency_by_name(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY_BY_NAME, (name,))
        return cursor.fetchone()


def get_agencies():
    with connection:
        cursor = connection.execute(GET_AGENCIES)
        return cursor.fetchall()


def get_agency_id_from_name(name: str):
    with connection:
        cursor = connection.execute(GET_AGENCY_ID_BY_NAME, (name,))
        return cursor.fetchall()


def get_prices():
    with connection:
        cursor = connection.execute(GET_PRICES)
        return cursor.fetchall()


def get_prices_by_property_id(property_id: int):
    with connection:
        cursor = connection.execute(GET_PRICES_BY_PROPERTY_ID, (property_id,))
        return cursor.fetchall()


def get_old_prices():
    with connection:
        cursor = connection.execute(GET_OLD_PRICES)
        return cursor.fetchall()


def update_description(property_id: int,
                       year_of_construction: float,
                       exposition: str,
                       floor: int,
                       total_floor_number: int,
                       neighborhood_description: str,
                       bedroom_number: int,
                       toilet_number: int,
                       bathroom_number: int,
                       cellar: bool,
                       lock_up_garage: bool,
                       heating: bool,
                       tv_cable: bool,
                       fireplace: bool,
                       digicode: bool,
                       intercom: bool,
                       elevator: bool,
                       fibre_optics_status: str,
                       garden: bool,
                       car_park_number: int,
                       balcony: bool,
                       large_balcony: bool,
                       estate_agency_fee_percentage: float,
                       pinel: bool,
                       denormandie: bool,
                       announce_publication: float,
                       announce_last_modification: float,
                       dpe_date: float,
                       energetic_performance_letter: str,
                       energetic_performance_number: int,
                       climatic_performance_number: int,
                       climatic_performance_letter: str,
                       estate_agency_id: int):
    try:
        with connection:
            connection.execute(UPDATE_DESCRIPTION, (year_of_construction,
                                                    exposition, floor,
                                                    total_floor_number,
                                                    neighborhood_description,
                                                    bedroom_number,
                                                    toilet_number,
                                                    bathroom_number,
                                                    cellar,
                                                    lock_up_garage,
                                                    heating,
                                                    tv_cable,
                                                    fireplace,
                                                    digicode,
                                                    intercom,
                                                    elevator,
                                                    fibre_optics_status,
                                                    garden,
                                                    car_park_number,
                                                    balcony,
                                                    large_balcony,
                                                    estate_agency_fee_percentage,
                                                    pinel,
                                                    denormandie,
                                                    announce_publication,
                                                    announce_last_modification,
                                                    dpe_date,
                                                    energetic_performance_letter,
                                                    energetic_performance_number,
                                                    climatic_performance_number,
                                                    climatic_performance_letter,
                                                    estate_agency_id,
                                                    property_id)
                               )
        print(f"OK : Description for Property {property_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error updating description for Property {property_id}: {e}")


def update_agency(id: int,
                  name: str,
                  address: str,
                  fee_percentage: int,
                  evaluation: str,
                  total_announces: int,
                  total_announces_active: int
                  ):
    try:
        with connection:
            connection.execute(UPDATE_AGENCY, (id,
                                               name,
                                               address,
                                               fee_percentage,
                                               evaluation,
                                               total_announces,
                                               total_announces_active))
        print(f"OK : Agency {name} updated successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error updating agency {name}: {e}")


def update_agency_totals(agency_id: int):
    try:
        with connection:
            connection.execute(UPDATE_AGENCY_TOTALS, (agency_id,))
        print(f"""OK: Both total_announces_active and total_announces
              incremented successfully for agency ID {agency_id}.""")
    except sqlite3.Error as e:
        print(f"KO: Error updating totals for agency ID {agency_id}: {e}")


def update_total_active_decrement(agency_id: int):
    try:
        with connection:
            connection.execute(UPDATE_AGENCY_TOTAL_ACTIVE_DECREMENT, (agency_id,))
        print(f"OK: total_announces_active decremented successfully for agency ID {agency_id}.")
    except sqlite3.Error as e:
        print(f"KO: Error decrementing total_announces_active for agency ID {agency_id}: {e}")


def delete_property(id: int):
    try:
        with connection:
            connection.execute(DELETE_PROPERTY, (id, ))
        print(f"OK : Property {id} has been deleted successfully.")
    except sqlite3.Error as e:
        print(f"KO : Error deleting property {id}: {e}")
