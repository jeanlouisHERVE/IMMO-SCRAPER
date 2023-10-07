import unittest
# from modules.add_announces import add_new_announces, add_descriptions
# from modules.update import update_descriptions


class TestMyModules(unittest.TestCase):
    def test_add_new_announces(self):
        print("some text")

    def test_add_descriptions(self):
        print("some text")


if __name__ == '__main__':
    unittest.main()

# Define the order of tests
    ordered_tests = [
        "test_add_new_announces",
        "test_add_descriptions",
    ]

    test_instance = TestMyModules()
    ordered_suite = unittest.TestSuite()

    for test_name in ordered_tests:
        ordered_suite.addTest(test_instance.findTest(test_instance, test_name))

    runner = unittest.TextTestRunner()
    runner.run(ordered_suite)
