
import os
import unittest
import tempfile

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
    update_property,
    update_description,
    update_agency,
    delete_property
)

# get data from .env file
load_dotenv()


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_fd, self.db_path = tempfile.mkstemp()

        # Create the database tables before running tests
        create_tables()

    def tearDown(self):
        # Close and remove the temporary database file
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_add_property(self):
        # Add a property to the database
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example.com",
            4,
            200,
            1234567890.0
        )

        # Get the added property by its ID
        property_data = get_property_by_id(property_id)

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data[0], property_id)
        self.assertEqual(property_data[1], "House")
        self.assertEqual(property_data[2], "Paris")
        self.assertEqual(property_data[3], "District A")
        self.assertEqual(property_data[4], "75001")
        self.assertEqual(property_data[5], "example.com")
        self.assertEqual(property_data[6], 4)
        self.assertEqual(property_data[7], 200)
        self.assertEqual(property_data[8], 1234567890.0)

    def test_add_old_property(self):
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
        self.cursor.execute("SELECT * FROM old_properties WHERE id = ?", (last_inserted_id,))
        property_record = self.cursor.fetchone()
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

    def test_add_description(self):
        # Add a property first
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example.com",
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
        self.assertEqual(description_data[32], 1)  # estate_agency_id

    def test_add_agency(self):
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
        self.assertEqual(agency_data[0], "ABC Real Estate")  # name
        self.assertEqual(agency_data[1], "123 Main St")  # address
        self.assertEqual(agency_data[2], 5)  # fee_percentage
        self.assertEqual(agency_data[3], "Excellent")  # evaluation

    def test_add_price_to_property(self):
        # Add a price to a property
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example.com",
            4,
            200,
            1234567890.0
        )

        add_price_to_property(1234567890.0, property_id, 500000)

        # Retrieve the added price for the property
        price_data = get_property_prices(property_id)

        # Check if the retrieved price matches the added data
        self.assertIsNotNone(price_data)
        self.assertEqual(price_data[0], 1234567890.0)  # date
        self.assertEqual(price_data[1], property_id)  # property_id
        self.assertEqual(price_data[2], 500000)  # price

    def test_get_property_by_url(self):
        # Add a property to the database
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example.com",
            4,
            200,
            1234567890.0
        )

        # Get the added property by its URL
        property_data = get_property_by_url("example.com")

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data[0], property_id)  # id
        self.assertEqual(property_data[1], "House")  # type_of_property
        self.assertEqual(property_data[2], "Paris")  # town
        self.assertEqual(property_data[3], "District A")  # district
        self.assertEqual(property_data[4], "75001")  # postcode
        self.assertEqual(property_data[5], "example.com")  # url
        self.assertEqual(property_data[6], 4)  # room_number
        self.assertEqual(property_data[7], 200)  # surface
        self.assertEqual(property_data[8], 1234567890.0)  # date_add_to_d

    def test_get_property_by_id(self):
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

    def test_get_id_url_from_properties(self):
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

        # Get ID and URL data from properties
        id_url_data = get_id_url_from_properties()

        # Check if the retrieved data matches the added properties
        self.assertIsNotNone(id_url_data)
        self.assertIsInstance(id_url_data, list)
        self.assertEqual(len(id_url_data), 2)

        # Check the data for the first property
        self.assertIn((property_id1, "example1.com"), id_url_data)

        # Check the data for the second property
        self.assertIn((property_id2, "example2.com"), id_url_data)

    def test_get_id_url_dateofmodification_from_properties(self):
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

        # Get ID, URL, and date of modification data from properties
        id_url_date_data = get_id_url_dateofmodification_from_properties()

        # Check if the retrieved data matches the added properties
        self.assertIsNotNone(id_url_date_data)
        self.assertIsInstance(id_url_date_data, list)
        self.assertEqual(len(id_url_date_data), 2)

        # Check the data for the first property
        expected_data1 = (property_id1, "example1.com", None)  # Assuming no date for the first property
        self.assertIn(expected_data1, id_url_date_data)

        # Check the data for the second property
        expected_data2 = (property_id2, "example2.com", None)  # Assuming no date for the second property
        self.assertIn(expected_data2, id_url_date_data)

    def test_get_properties(self):
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

        # Check if the retrieved properties match the added ones
        self.assertIsNotNone(properties)
        self.assertIsInstance(properties, list)
        self.assertEqual(len(properties), 2)

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

    def test_get_properties_number(self):
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

        # Check if the retrieved count matches the number of added properties (2 in this case)
        self.assertEqual(properties_count, 2)

    def test_get_properties_from_adding_date(self):
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

        # Check if the number of retrieved properties matches the expected count (2 in this case)
        self.assertEqual(len(properties), 2)

        # You can further assert properties individually if needed
        for property_data in properties:
            self.assertEqual(property_data["date_add_to_db"], target_date)

    def test_get_property_description_by_id(self):
        # Add a property to the database
        property_id = add_property(
            "House",
            "Paris",
            "District A",
            "75001",
            "example.com",
            4,
            200,
            1234567890.0
        )

        # Add a property description for the added property
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
            5.0,
            True,
            True,
            "2023-09-14",
            "2023-09-14",
            "2023-09-14",
            "C",
            100,
            150,
            "D",
            1
        )

        # Retrieve the property description by its ID
        property_description = get_property_description_by_id(property_id)

        # Check if the retrieved property description matches the added data
        self.assertIsNotNone(property_description)
        self.assertEqual(property_description["property_id"], property_id)
        self.assertEqual(property_description["year_of_construction"], 1990.0)
        self.assertEqual(property_description["exposition"], "North")
        self.assertEqual(property_description["floor"], 2)
        self.assertEqual(property_description["total_floor_number"], 5)
        self.assertEqual(property_description["neighborhood_description"], "Quiet neighborhood")
        self.assertEqual(property_description["bedroom_number"], 3)
        self.assertEqual(property_description["toilet_number"], 2)
        self.assertEqual(property_description["bathroom_number"], 2)
        self.assertTrue(property_description["cellar"])
        self.assertFalse(property_description["lock_up_garage"])
        self.assertTrue(property_description["heating"])
        self.assertFalse(property_description["tv_cable"])
        self.assertTrue(property_description["fireplace"])
        self.assertFalse(property_description["digicode"])
        self.assertTrue(property_description["intercom"])
        self.assertFalse(property_description["elevator"])
        self.assertEqual(property_description["fibre_optics_status"], "Fiber optics available")
        self.assertTrue(property_description["garden"])
        self.assertEqual(property_description["car_park_number"], 1)
        self.assertTrue(property_description["balcony"])
        self.assertFalse(property_description["large_balcony"])
        self.assertEqual(property_description["estate_agency_fee_percentage"], 5.0)
        self.assertTrue(property_description["pinel"])
        self.assertTrue(property_description["denormandie"])
        self.assertEqual(property_description["announce_publication"], "2023-09-14")
        self.assertEqual(property_description["announce_last_modification"], "2023-09-14")
        self.assertEqual(property_description["dpe_date"], "2023-09-14")
        self.assertEqual(property_description["energetic_performance_letter"], "C")
        self.assertEqual(property_description["energetic_performance_number"], 100)
        self.assertEqual(property_description["climatic_performance_number"], 150)
        self.assertEqual(property_description["climatic_performance_letter"], "D")
        self.assertEqual(property_description["estate_agency_id"], 1)

    def test_get_agency(self):
        # Add an agency to the database
        add_agency("ABC Realty", "123 Main St", 5, "Good")

        # Retrieve the added agency by its name
        agency = get_agency("ABC Realty")

        # Check if the retrieved agency matches the added data
        self.assertIsNotNone(agency)
        self.assertEqual(agency["name"], "ABC Realty")
        self.assertEqual(agency["address"], "123 Main St")
        self.assertEqual(agency["fee_percentage"], 5)
        self.assertEqual(agency["evaluation"], "Good")

    def test_get_agencies(self):
        # Call the function to retrieve agencies
        agencies = get_agencies()

        # Check if the function returns a list
        self.assertIsInstance(agencies, list)

        # Check if the number of retrieved agencies matches the number of inserted test data
        self.assertEqual(len(agencies), 3)

        # Check if the retrieved agency data is a tuple with the correct structure
        for agency in agencies:
            self.assertIsInstance(agency, tuple)
            self.assertEqual(len(agency), 4)

        # Check if the retrieved agency data matches the inserted test data
        self.assertIn(('Agency1', 'Address1', 5, 'Good'), agencies)
        self.assertIn(('Agency2', 'Address2', 7, 'Excellent'), agencies)
        self.assertIn(('Agency3', 'Address3', 6, 'Average'), agencies)

    def test_get_agency_id_from_name(self):
        # Add an agency to the database
        add_agency("Agency1", "123 Main St", 5, "Good")

        # Retrieve the agency ID by name
        agency_id = get_agency_id_from_name("Agency1")

        # Check if the retrieved agency ID is not empty and matches the added agency's ID
        self.assertIsNotNone(agency_id)
        self.assertIsInstance(agency_id, list)
        self.assertEqual(len(agency_id), 1)
        self.assertEqual(agency_id[0]["id"], 1)

    def test_update_description(self):
        # Call the function to update description
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
        self.cursor.execute("SELECT * FROM descriptions WHERE property_id = ?", (1,))
        updated_description = self.cursor.fetchone()

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
        self.assertEqual(updated_description[11], 0)
        self.assertEqual(updated_description[12], 0)
        self.assertEqual(updated_description[13], 1)
        self.assertEqual(updated_description[14], 1)
        self.assertEqual(updated_description[15], 1)
        self.assertEqual(updated_description[16], 'Fiber not available')
        self.assertEqual(updated_description[17], 0)
        self.assertEqual(updated_description[18], 1)
        self.assertEqual(updated_description[19], 0)
        self.assertEqual(updated_description[20], 1)
        self.assertEqual(updated_description[21], 0)
        self.assertEqual(updated_description[22], 0)
        self.assertEqual(updated_description[23], 1)
        self.assertEqual(updated_description[24], '2023-09-17')
        self.assertEqual(updated_description[25], '2023-09-18')
        self.assertEqual(updated_description[26], '2023-09-19')
        self.assertEqual(updated_description[27], 'B')
        self.assertEqual(updated_description[28], 150)
        self.assertEqual(updated_description[29], 250)
        self.assertEqual(updated_description[30], 'C')
        self.assertEqual(updated_description[31], 2)

    def test_update_agency(self):
        # Call the function to update agency
        update_agency('Agency1', '456 Elm St', 6, 'Excellent')

        # Query the updated agency from the database
        self.cursor.execute("SELECT * FROM agencies WHERE name = ?", ('Agency1',))
        updated_agency = self.cursor.fetchone()

        # Check if the agency fields have been updated correctly
        self.assertEqual(updated_agency[1], 'Agency1')
        self.assertEqual(updated_agency[2], '456 Elm St')
        self.assertEqual(updated_agency[3], 6)
        self.assertEqual(updated_agency[4], 'Excellent')

    def test_delete_property(self):
        # Call the function to delete a property
        delete_property(1)

        # Query the properties from the database
        self.cursor = self.cursor.execute("SELECT * FROM properties WHERE id = ?", (1,))
        deleted_property = self.cursor.fetchone()

        # Check if the property has been deleted
        self.assertIsNone(deleted_property)

    def test_delete_nonexistent_property(self):
        # Call the function to delete a nonexistent property
        delete_property(3)

        # Query the properties from the database
        self.cursor.execute("SELECT * FROM properties WHERE id = ?", (10000,))
        nonexistent_property = self.cursor.fetchone()

        # Check if no property was deleted
        self.assertIsNone(nonexistent_property)


if __name__ == '__main__':
    unittest.main()
