
import os
import unittest
import tempfile
from dotenv import load_dotenv
from modules.database_app import (
    create_tables,
    add_property,
    add_description,
    add_agency,
    get_agency,
    get_property_by_id,
    get_property_description_by_id,
    update_property
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

    def test_update_property(self):
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

        # Update the price of the property
        update_property(property_id, 500000)

        # Get the updated property
        property_data = get_property_by_id(property_id)

        # Check if the price has been updated
        self.assertEqual(property_data[9], 500000)


if __name__ == '__main__':
    unittest.main()
