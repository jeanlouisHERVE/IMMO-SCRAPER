import unittest
import tempfile
import os
from modules.database_app import create_tables, add_property, get_property_by_id, update_property

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.environ["DATABASE_PATH"] = self.db_path
        
        # Create the database tables before running tests
        create_tables()

    def tearDown(self):
        # Close and remove the temporary database file
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_add_and_get_property(self):
        # Add a property to the database
        property_id = add_property("House", "Paris", "District A", "75001", "example.com", 4, 200, 1234567890.0)

        # Get the added property by its ID
        property_data = get_property_by_id(property_id)

        # Check if the retrieved property matches the added data
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data["id"], property_id)
        self.assertEqual(property_data["type_of_property"], "House")
        self.assertEqual(property_data["town"], "Paris")
        self.assertEqual(property_data["district"], "District A")
        self.assertEqual(property_data["postcode"], "75001")
        self.assertEqual(property_data["url"], "example.com")
        self.assertEqual(property_data["room_number"], 4)
        self.assertEqual(property_data["surface"], 200)
        self.assertEqual(property_data["date_add_to_db"], 1234567890.0)

    def test_update_property(self):
        # Add a property to the database
        property_id = add_property("Apartment", "Paris", "District B", "75002", "example2.com", 2, 100, 1234567890.0)

        # Update the price of the property
        update_property(property_id, 500000)

        # Get the updated property
        property_data = get_property_by_id(property_id)

        # Check if the price has been updated
        self.assertEqual(property_data["price"], 500000)

if __name__ == '__main__':
    unittest.main()