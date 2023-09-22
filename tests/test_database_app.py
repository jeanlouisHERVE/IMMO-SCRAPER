import unittest
import sqlite3

from dotenv import load_dotenv
from modules.database_app import (
    create_tables,
    add_property,
    add_old_property,
    add_description,
    add_agency,
    add_price_to_property,
    get_property_by_url,
    get_property_by_id,
    get_old_property_by_id,
    get_id_url_from_properties,
    get_id_url_dateofmodification_from_properties,
    get_properties,
    get_properties_number,
    get_properties_from_adding_date,
    get_property_prices,
    get_property_description_by_id,
    get_agency,
    get_agencies,
    get_agency_id_from_name,
    update_description,
    update_agency,
    delete_property,
    delete_tables
)

# get data from .env file
load_dotenv()


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.database_connection = sqlite3.connect(":memory:")

        self.cursor = self.database_connection.cursor()

        # Create the database tables before running tests
        create_tables()

    def reset_database(self):
        try:
            delete_tables(self.database_connection)
            print("Database reset successfully.")
        except sqlite3.Error as e:
            print(f"Error resetting the database: {e}")

    def tearDown(self):
        try:
            # Reset the database before closing the connection
            print("Resetting database")
            self.reset_database()
        except Exception as e:
            print(f"Error resetting the database: {e}")

        # Close the database connection
        print("Closing database")
        self.database_connection.close()
        print("-------------------------------------------------------")

    def test_01_add_property(self):
        # Add a property to the database
        print("DATABASE TEST N°1 : test_add_property")
        property_id = add_property(
            "House",
            "Sartrouville",
            "District P",
            "78500",
            "e.com",
            3,
            180,
            1234567890.0
        )

        # Get the added property by its ID
        property_data = get_property_by_id(property_id)

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data[0], property_id)
        self.assertEqual(property_data[1], "House")
        self.assertEqual(property_data[2], "Sartrouville")
        self.assertEqual(property_data[3], "District P")
        self.assertEqual(property_data[4], "78500")
        self.assertEqual(property_data[5], "e.com")
        self.assertEqual(property_data[6], 3)
        self.assertEqual(property_data[7], 180)
        self.assertEqual(property_data[8], 1234567890.0)

    def test_02_add_old_property(self):
        print("DATABASE TEST N°2 : test_add_old_property")
        # Test data
        type_of_property = "Apartment"
        town = "Test Town"
        district = "Test District"
        postcode = "12345"
        url = "http://example.com/property"
        room_number = 3
        surface = 100
        date_add_to_db = 1631590200.0  # Replace with your desired timestamp

        # Call the function to add an old property
        last_inserted_id = add_old_property(
            type_of_property, town, district, postcode, url, room_number, surface, date_add_to_db)

        # Check if the property was added successfully
        self.assertIsNotNone(last_inserted_id)

        # Check if the property exists in the database
        property_record = get_old_property_by_id(last_inserted_id)
        self.assertIsNotNone(property_record)

        # Check if the retrieved property data matches the inserted data
        self.assertEqual(property_record[1], type_of_property)
        self.assertEqual(property_record[2], town)
        self.assertEqual(property_record[3], district)
        self.assertEqual(property_record[4], postcode)
        self.assertEqual(property_record[5], url)
        self.assertEqual(property_record[6], room_number)
        self.assertEqual(property_record[7], surface)
        self.assertEqual(property_record[8], date_add_to_db)

    def test_03_add_description(self):
        print("DATABASE TEST N°3 : test_add_description")
        # Add a property first
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "c.com",
            4,
            200,
            1234567890.0
        )

        # Add a description for the property
        add_description(
            property_id,
            1990.0,
            "North",
            2,
            5,
            "Quiet neighborhood",
            3,
            2,
            2,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            "Fiber available",
            True,
            1,
            True,
            False,
            5.0,
            True,
            True,
            "01/01/2023",
            "01/01/2023",
            "01/01/2023",
            "C",
            150,
            120,
            "D",
            1
        )

        # Get the added description by property ID
        description_data = get_property_description_by_id(property_id)

        # Check if the retrieved description matches the added data
        self.assertIsNotNone(description_data)
        self.assertEqual(description_data[0], property_id)  # property_id
        self.assertEqual(description_data[1], 1990.0)  # year_of_construction
        self.assertEqual(description_data[2], "North")  # exposition
        self.assertEqual(description_data[3], 2)  # floor
        self.assertEqual(description_data[4], 5)  # total_floor_number
        self.assertEqual(description_data[5], "Quiet neighborhood")  # neighborhood_description
        self.assertEqual(description_data[6], 3)  # bedroom_number
        self.assertEqual(description_data[7], 2)  # toilet_number
        self.assertEqual(description_data[8], 2)  # bathroom_number
        self.assertTrue(description_data[9])  # cellar
        self.assertFalse(description_data[10])  # lock_up_garage
        self.assertTrue(description_data[11])  # heating
        self.assertTrue(description_data[12])  # tv_cable
        self.assertFalse(description_data[13])  # fireplace
        self.assertFalse(description_data[14])  # digicode
        self.assertTrue(description_data[15])  # intercom
        self.assertFalse(description_data[16])  # elevator
        self.assertEqual(description_data[17], "Fiber available")  # fibre_optics_status
        self.assertTrue(description_data[18])  # garden
        self.assertEqual(description_data[19], 1)  # car_park_number
        self.assertTrue(description_data[20])  # balcony
        self.assertFalse(description_data[21])  # large_balcony
        self.assertEqual(description_data[22], 5.0)  # estate_agency_fee_percentage
        self.assertTrue(description_data[23])  # pinel
        self.assertTrue(description_data[24])  # denormandie
        self.assertEqual(description_data[25], "01/01/2023")  # announce_publication
        self.assertEqual(description_data[26], "01/01/2023")  # announce_last_modification
        self.assertEqual(description_data[27], "01/01/2023")  # dpe_date
        self.assertEqual(description_data[28], "C")  # energetic_performance_letter
        self.assertEqual(description_data[29], 150)  # energetic_performance_number
        self.assertEqual(description_data[30], 120)  # climatic_performance_number
        self.assertEqual(description_data[31], "D")  # climatic_performance_letter
        self.assertEqual(description_data[32], 1)

    def test_04_add_agency(self):
        print("DATABASE TEST N°4 : test_add_description")
        # Add an agency
        add_agency(
            "ABC Real Estate",
            "123 Main St",
            5,
            "Excellent"
        )

        # Get the added agency by its name
        agency_data = get_agency("ABC Real Estate")

        # Check if the retrieved agency matches the added data
        self.assertIsNotNone(agency_data)
        self.assertEqual(agency_data[0], 1)  # id
        self.assertEqual(agency_data[1], "ABC Real Estate")  # name
        self.assertEqual(agency_data[2], "123 Main St")  # address
        self.assertEqual(agency_data[3], 5)  # fee_percentage
        self.assertEqual(agency_data[4], "Excellent")

    def test_05_add_price_to_property(self):
        print("DATABASE TEST N°5 : test_add_price_to_property")
        # Add a price to a property
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "b.com",
            4,
            200,
            1234567890.0
        )

        add_price_to_property(1234567890.0, property_id, 500000)

        # Retrieve the added price for the property
        price_data = get_property_prices(property_id)
        print("price_data", price_data)
        print("TEST 5 price_data[0]", price_data[0])

        # Check if the retrieved price matches the added data
        self.assertIsNotNone(price_data)
        self.assertEqual(price_data[0], 1)  # id
        self.assertEqual(price_data[1], 1234567890.0)  # date
        self.assertEqual(price_data[2], property_id)  # property_id
        self.assertEqual(price_data[3], 500000)

    def test_06_get_property_by_url(self):
        print("DATABASE TEST N°6 : test_get_property_by_url")
        # Add a property to the database
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "a.com",
            4,
            200,
            1234567890.0
        )

        # Get the added property by its URL
        property_data = get_property_by_url("a.com")

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data[0], property_id)  # id
        self.assertEqual(property_data[1], "House")  # type_of_property
        self.assertEqual(property_data[2], "Paris")  # town
        self.assertEqual(property_data[3], "District A")  # district
        self.assertEqual(property_data[4], "75001")  # postcode
        self.assertEqual(property_data[5], "a.com")  # url
        self.assertEqual(property_data[6], 4)  # room_number
        self.assertEqual(property_data[7], 200)  # surface
        self.assertEqual(property_data[8], 1234567890.0)  # date_add_to_d

    def test_07_get_property_by_id(self):
        print("DATABASE TEST N°7 : test_get_property_by_id")
        # Add a property to the database
        property_id = add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        # Get the added property by its ID
        property_data = get_property_by_id(property_id)

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data[0], property_id)  # id
        self.assertEqual(property_data[1], "Apartment")  # type_of_property
        self.assertEqual(property_data[2], "Paris")  # town
        self.assertEqual(property_data[3], "District B")  # district
        self.assertEqual(property_data[4], "75002")  # postcode
        self.assertEqual(property_data[5], "example2.com")  # url
        self.assertEqual(property_data[6], 2)  # room_number
        self.assertEqual(property_data[7], 100)  # surface
        self.assertEqual(property_data[8], 1234567890.0)  # date_add_to_db

    def test_08_get_id_url_from_properties(self):
        print("DATABASE TEST N°8 : test_get_id_url_from_properties")
        # Add properties to the database
        property_id1 = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )
        property_id2 = add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        properties_number = get_properties_number()[0][0]
        # Get ID and URL data from properties
        id_url_data = get_id_url_from_properties()

        # Check if the retrieved data matches the added properties
        self.assertIsNotNone(id_url_data)
        self.assertIsInstance(id_url_data, list)
        self.assertEqual(len(id_url_data), properties_number)

        # Check the data for the first property
        self.assertIn((property_id1, "example1.com"), id_url_data)

        # Check the data for the second property
        self.assertIn((property_id2, "example2.com"), id_url_data)

    def test_09_get_id_url_dateofmodification_from_properties(self):
        print("DATABASE TEST N°9 : test_get_id_url_dateofmodification_from_properties")
        # Add properties to the database
        property_id1 = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )

        add_description(
            property_id1,
            1990.0,
            "North",
            2,
            5,
            "Quiet neighborhood",
            3,
            2,
            2,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            "Fiber available",
            True,
            1,
            True,
            False,
            5.0,
            True,
            True,
            "01/01/2023",
            "01/01/2023",
            "01/01/2023",
            "C",
            150,
            120,
            "D",
            1
        )
        property_id2 = add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        add_description(
            property_id2,
            1990.0,
            "North",
            2,
            5,
            "Quiet neighborhood",
            3,
            2,
            2,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            "Fiber available",
            True,
            1,
            True,
            False,
            5.0,
            True,
            True,
            "01/01/2023",
            "01/01/2023",
            "01/01/2023",
            "C",
            150,
            120,
            "D",
            1
        )

        properties_number = get_properties_number()[0][0]
        print("TEST 9 properties_number", properties_number)
        # Get ID, URL, and date of modification data from properties
        properties_data = get_properties()
        print("TEST 9 properties_data", properties_data)
        print("TEST 9 len(properties_data)", len(properties_data))

        id_url_date_data = get_id_url_dateofmodification_from_properties()
        print("TEST 9 id_url_date_data", id_url_date_data)

        # Check if the retrieved data matches the added properties
        self.assertIsNotNone(id_url_date_data)
        self.assertIsInstance(id_url_date_data, list)
        self.assertEqual(len(id_url_date_data), 3)

        # Check the data for the first property
        expected_data1 = (property_id1, "example1.com", "01/01/2023")  # Assuming no date for the first property
        self.assertIn(expected_data1, id_url_date_data)

        # Check the data for the second property
        expected_data2 = (property_id2, "example2.com", "01/01/2023")  # Assuming no date for the second property
        self.assertIn(expected_data2, id_url_date_data)

    def test_10_get_properties(self):
        print("DATABASE TEST N°10 : test_get_properties")
        # Add some properties to the database
        property1_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )
        property2_id = add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        # Retrieve all properties from the database
        properties = get_properties()
        print("properties", properties)

        # Check if the retrieved properties match the added ones
        self.assertIsNotNone(properties)
        self.assertIsInstance(properties, list)
        self.assertEqual(len(properties), 11)

        # Check the data for the first property
        property1_data = (
            property1_id,
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )
        self.assertIn(property1_data, properties)

        # Check the data for the second property
        property2_data = (
            property2_id,
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )
        self.assertIn(property2_data, properties)

    def test_11_get_properties_number(self):
        print("DATABASE TEST N°11 : test_get_properties_number")
        # Add some properties to the database
        add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )
        add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        # Retrieve the number of properties from the database
        properties_count = get_properties_number()

        # Extract the count value from the result
        count_value = properties_count[0][0]

        # Check if the retrieved count matches the number of added properties (2 in this case)
        self.assertEqual(count_value, 13)

    def test_12_get_properties_from_adding_date(self):
        print("DATABASE TEST N°12 : test_get_properties_from_adding_date")
        # Add some properties with a specific date_add_to_db value to the database
        add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example1.com",
            4,
            200,
            1234567890.0
        )
        add_property(
            "Apartment",
            "Paris",
            "District B",
            "75002",
            "example2.com",
            2,
            100,
            1234567890.0
        )

        # Specify the date_add_to_db value for filtering
        target_date = 1234567890.0

        # Retrieve properties with the specified date_add_to_db value from the database
        properties = get_properties_from_adding_date(target_date)

        print("properties", properties)
        # Check if the number of retrieved properties matches the expected count (2 in this case)
        self.assertEqual(len(properties), 15)

        # You can further assert properties individually if needed
        for property_data in properties:
            print("TEST 12 property_data", property_data)
            self.assertEqual(property_data[8], target_date)

    def test_13_get_property_description_by_id(self):
        print("DATABASE TEST N°13 : test_get_property_description_by_id")
        # Add a property to the database
        property_id = add_property(
            "Appartement",
            "Sartrouville",
            "L'Union",
            "78500",
            "https://www.bienici.com/annonce/vente/sartrouville",
            4,
            200,
            1695034738.6352
        )

        # Add a property description for the added property
        add_description(
            property_id,
            -662688000.0,
            "Sud",
            2,
            5,
            """La Vaudoire Centre-ville est un quartier de la ville
            de Sartrouville situé dans le département des Yvelines (78).
            Les 4 781 habitants de ce quartier (sur les 51 713 de la commune)
            ont un âge moyen de 41 ans. La catégorie socio-professionnelle
            la plus représentée dans le quartier est celle des cadres. Côté
            immobilier, les habitations du quartier sont réparties en 38 % de
            maisons et 62 % d'appartements. La part de logements sociaux est
            ici de 3 %. La taxe d'habitation s'élève à 14 % et la taxe foncière
            à 12 % (en moyenne pour le département : taxe d'habitation à 19 %,
            taxe foncière à 8 %). Quant à la taxe d'enlèvement des ordures
            ménagères, elle est de 6 % .""",
            3,
            2,
            2,
            True,
            False,
            "radiateur gaz individuel",
            False,
            True,
            False,
            True,
            False,
            "Fiber optics available",
            True,
            1,
            True,
            False,
            5,
            True,
            True,
            1693958400,
            1695034738.6352,
            1645056000,
            "C",
            100,
            150,
            "D",
            1
        )

        # Retrieve the property description by its ID
        description_data = get_property_description_by_id(property_id)
        print("TEST 13 description_data", description_data)

        # Check if the retrieved description matches the added data
        self.assertIsNotNone(description_data)
        self.assertEqual(description_data[0], property_id)  # property_id
        self.assertEqual(description_data[1], -662688000.0)  # year_of_construction
        self.assertEqual(description_data[2], "Sud")  # exposition
        self.assertEqual(description_data[3], 2)  # floor
        self.assertEqual(description_data[4], 5)  # total_floor_number
        self.assertEqual(description_data[5], """La Vaudoire Centre-ville est un quartier de la ville
            de Sartrouville situé dans le département des Yvelines (78).
            Les 4 781 habitants de ce quartier (sur les 51 713 de la commune)
            ont un âge moyen de 41 ans. La catégorie socio-professionnelle
            la plus représentée dans le quartier est celle des cadres. Côté
            immobilier, les habitations du quartier sont réparties en 38 % de
            maisons et 62 % d'appartements. La part de logements sociaux est
            ici de 3 %. La taxe d'habitation s'élève à 14 % et la taxe foncière
            à 12 % (en moyenne pour le département : taxe d'habitation à 19 %,
            taxe foncière à 8 %). Quant à la taxe d'enlèvement des ordures
            ménagères, elle est de 6 % .""")  # neighborhood_description
        self.assertEqual(description_data[6], 3)  # bedroom_number
        self.assertEqual(description_data[7], 2)  # toilet_number
        self.assertEqual(description_data[8], 2)  # bathroom_number
        self.assertEqual(description_data[9], 1)  # cellar
        self.assertEqual(description_data[10], 0)  # lock_up_garage
        self.assertTrue(description_data[11], "radiateur gaz individuel")  # heating
        self.assertEqual(description_data[12], 0)  # tv_cable
        self.assertEqual(description_data[13], 1)  # fireplace
        self.assertEqual(description_data[14], 0)  # digicode
        self.assertEqual(description_data[15], 1)  # intercom
        self.assertEqual(description_data[16], 0)  # elevator
        self.assertEqual(description_data[17], "Fiber optics available")  # fibre_optics_status
        self.assertEqual(description_data[18], 1)  # garden
        self.assertEqual(description_data[19], 1)  # car_park_number
        self.assertEqual(description_data[20], 1)  # balcony
        self.assertEqual(description_data[21], 0)  # large_balcony
        self.assertEqual(description_data[22], 5)  # estate_agency_fee_percentage
        self.assertEqual(description_data[23], 1)  # pinel
        self.assertEqual(description_data[24], 1)  # denormandie
        self.assertEqual(description_data[25], 1693958400)  # announce_publication
        self.assertEqual(description_data[26], 1695034738.6352)  # announce_last_modification
        self.assertEqual(description_data[27], 1645056000)  # dpe_date
        self.assertEqual(description_data[28], "C")  # energetic_performance_letter
        self.assertEqual(description_data[29], 100)  # energetic_performance_number
        self.assertEqual(description_data[30], 150)  # climatic_performance_number
        self.assertEqual(description_data[31], "D")  # climatic_performance_letter
        self.assertEqual(description_data[32], 1)  # estate_agency_id

    def test_14_get_agency(self):
        print("DATABASE TEST N°14 : test_get_agency")
        # Add an agency to the database
        add_agency("ABC Realty", "123 Main St", 5, "Good")

        # Retrieve the added agency by its name
        agency = get_agency("ABC Realty")

        # Check if the retrieved agency matches the added data
        self.assertIsNotNone(agency)
        self.assertEqual(agency[1], "ABC Realty")
        self.assertEqual(agency[2], "123 Main St")
        self.assertEqual(agency[3], 5)
        self.assertEqual(agency[4], "Good")

    def test_15_get_agencies(self):
        print("DATABASE TEST N°15 : test_get_agencies")

        add_agency(
            'A1',
            'Address1',
            5,
            'Good'
        )
        add_agency(
            'A2',
            'Address2',
            7,
            'Excellent'
        )
        add_agency(
            'A3',
            'Address3',
            6,
            'Average'
        )

        # Call the function to retrieve agencies
        agencies = get_agencies()
        print("TEST 15 len(agencies)", len(agencies))
        # Check if the function returns a list
        self.assertIsInstance(agencies, list)

        # Check if the number of retrieved agencies matches the number of inserted test data
        self.assertEqual(len(agencies), 5)

        # Check if the retrieved agency data is a tuple with the correct structure
        for agency in agencies:
            self.assertIsInstance(agency, tuple)
            self.assertEqual(len(agency), 5)

        # Check if the retrieved agency data matches the inserted test data
        self.assertIn((3, 'A1', 'Address1', 5, 'Good'), agencies)
        self.assertIn((4, 'A2', 'Address2', 7, 'Excellent'), agencies)
        self.assertIn((5, 'A3', 'Address3', 6, 'Average'), agencies)

    def test_16_get_agency_id_from_name(self):
        print("DATABASE TEST N°16 : test_get_agency_id_from_name")
        # Add an agency to the database
        add_agency("B1", "123 Main St", 5, "Good")

        # Retrieve the agency ID by name
        agency_id = get_agency_id_from_name("B1")

        # Check if the retrieved agency ID is not empty and matches the added agency's ID
        self.assertIsNotNone(agency_id)
        self.assertIsInstance(agency_id, list)
        self.assertEqual(len(agency_id), 1)
        self.assertEqual(agency_id[0][0], 6)

    def test_17_update_description(self):
        print("DATABASE TEST N°17 : test_update_description")
        # Call the function to update description
        properties = get_properties()
        print("TEST 17 properties", properties)
        property_description = get_property_description_by_id(1)
        print("TEST 17 property_description", property_description)

        add_description(
            1,
            -662688000.0,
            "Sud",
            2,
            5,
            """La Vaudoire Centre-ville est un quartier de la ville
            de Sartrouville situé dans le département des Yvelines (78).
            Les 4 781 habitants de ce quartier (sur les 51 713 de la commune)
            ont un âge moyen de 41 ans. La catégorie socio-professionnelle
            la plus représentée dans le quartier est celle des cadres. Côté
            immobilier, les habitations du quartier sont réparties en 38 % de
            maisons et 62 % d'appartements. La part de logements sociaux est
            ici de 3 %. La taxe d'habitation s'élève à 14 % et la taxe foncière
            à 12 % (en moyenne pour le département : taxe d'habitation à 19 %,
            taxe foncière à 8 %). Quant à la taxe d'enlèvement des ordures
            ménagères, elle est de 6 % .""",
            3,
            2,
            2,
            True,
            False,
            "radiateur gaz individuel",
            False,
            True,
            False,
            True,
            False,
            "Fiber optics available",
            True,
            1,
            True,
            False,
            5,
            True,
            True,
            1693958400,
            1695034738.6352,
            1645056000,
            "C",
            100,
            150,
            "D",
            1
        )

        update_description(1,
                           1999.0,
                           'South',
                           3,
                           6,
                           'Great neighborhood',
                           4,
                           3,
                           2,
                           0,
                           1,
                           "boiler",
                           0,
                           0,
                           1,
                           1,
                           1,
                           'Fiber not available',
                           0,
                           1,
                           0,
                           1,
                           0,
                           0,
                           1,
                           '2023-09-17',
                           '2023-09-18',
                           '2023-09-19',
                           'B',
                           150,
                           250,
                           'C',
                           2
                           )

        # Query the updated description from the database
        updated_description = get_property_description_by_id(1)
        print("TEST 17 updated_description", updated_description)

        # Check if the description fields have been updated correctly
        self.assertEqual(updated_description[1], 1999.0)
        self.assertEqual(updated_description[2], 'South')
        self.assertEqual(updated_description[3], 3)
        self.assertEqual(updated_description[4], 6)
        self.assertEqual(updated_description[5], 'Great neighborhood')
        self.assertEqual(updated_description[6], 4)
        self.assertEqual(updated_description[7], 3)
        self.assertEqual(updated_description[8], 2)
        self.assertEqual(updated_description[9], 0)
        self.assertEqual(updated_description[10], 1)
        self.assertEqual(updated_description[11], "boiler")
        self.assertEqual(updated_description[12], 0)
        self.assertEqual(updated_description[13], 0)
        self.assertEqual(updated_description[14], 1)
        self.assertEqual(updated_description[15], 1)
        self.assertEqual(updated_description[16], 1)
        self.assertEqual(updated_description[17], 'Fiber not available')
        self.assertEqual(updated_description[18], 0)
        self.assertEqual(updated_description[19], 1)
        self.assertEqual(updated_description[20], 0)
        self.assertEqual(updated_description[21], 1)
        self.assertEqual(updated_description[22], 0)
        self.assertEqual(updated_description[23], 0)
        self.assertEqual(updated_description[24], 1)
        self.assertEqual(updated_description[25], '2023-09-17')
        self.assertEqual(updated_description[26], '2023-09-18')
        self.assertEqual(updated_description[27], '2023-09-19')
        self.assertEqual(updated_description[28], 'B')
        self.assertEqual(updated_description[29], 150)
        self.assertEqual(updated_description[30], 250)
        self.assertEqual(updated_description[31], 'C')
        self.assertEqual(updated_description[32], 2)

    def test_18_update_agency(self):
        print("DATABASE TEST N°18 : test_update_agency")

        agency_id = add_agency(
                        "D3",
                        "123 Main St",
                        5,
                        "Excellent"
                        )
        agencies = get_agencies()
        print("TEST 18 agency_id", agency_id)
        print("TEST 18 agencies", agencies)
        # Call the function to update agency
        update_agency('D18', '456 Elm St', 6, 'Excellent', agency_id)

        # Query the updated agency from the database
        updated_agency = get_agency(agency_id)
        print("TEST 18 updated_agency", updated_agency)
        agencies = get_agencies()
        print("TEST 18 agencies", agencies)
        # Check if the agency fields have been updated correctly
        self.assertEqual(updated_agency[1], 'D18')
        self.assertEqual(updated_agency[2], '456 Elm St')
        self.assertEqual(updated_agency[3], 6)
        self.assertEqual(updated_agency[4], 'Excellent')

    def test_19_delete_property(self):
        print("DATABASE TEST N°19 : test_delete_property")

        property_id = add_property(
            "House",
            "Sartrouville",
            "District P",
            "78500",
            "f.com",
            3,
            180,
            1234567890.0
        )

        # Call the function to delete a property
        delete_property(property_id)

        # Query the properties from the database
        deleted_property = get_property_by_id(property_id)

        # Check if the property has been deleted
        self.assertIsNone(deleted_property)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabaseFunctions)

    # Define the order of tests
    ordered_tests = [
        "test_01_add_property",
        "test_02_add_old_property",
        "test_03_add_description",
        "test_04_add_agency",
        "test_05_add_price_to_property",
        "test_06_get_property_by_url",
        "test_07_get_property_by_id",
        "test_08_get_id_url_from_properties",
        "test_09_get_id_url_dateofmodification_from_properties",
        "test_10_get_properties",
        "test_11_get_properties_number",
        "test_12_get_properties_from_adding_date",
        "test_13_get_property_description_by_id",
        "test_14_get_agency",
        "test_15_get_agencies",
        "test_16_get_agency_id_from_name",
        "test_17_update_description",
        "test_18_update_agency",
        "test_19_delete_property",
    ]

    ordered_suite = unittest.TestSuite()
    for test_name in ordered_tests:
        ordered_suite.addTest(suite.findTestCases(TestDatabaseFunctions(test_name)))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
