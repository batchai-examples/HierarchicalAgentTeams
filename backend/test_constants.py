import unittest

class TestConstants(unittest.TestCase):
    """
    Test suite for the Constants class.
    This suite includes tests for the DATETIME_FORMAT constant and
    checks the immutability of the class attributes.
    """

    def test_datetime_format(self):
        """
        Test that the DATETIME_FORMAT constant is correctly defined.
        """
        # Check if the DATETIME_FORMAT is set to the expected format
        self.assertEqual(Constants.DATETIME_FORMAT, "%Y-%m-%d %H:%M:%S")

    def test_constant_immutable(self):
        """
        Test that attempting to change the DATETIME_FORMAT raises an error.
        """
        # Attempt to change the DATETIME_FORMAT constant
        with self.assertRaises(RuntimeError):
            Constants.DATETIME_FORMAT = "%d-%m-%Y"

    def test_invalid_constant_update(self):
        """
        Test that trying to update a constant raises a RuntimeError.
        """
        # Create an instance of Constants
        constants_instance = Constants()
        # Attempt to set a new attribute
        with self.assertRaises(RuntimeError):
            constants_instance.__setattr__('DATETIME_FORMAT', "%d-%m-%Y")

    def test_no_update_on_existing_attribute(self):
        """
        Test that trying to update an existing attribute raises a RuntimeError.
        """
        # Create an instance of Constants
        constants_instance = Constants()
        # Attempt to set an existing attribute
        with self.assertRaises(RuntimeError):
            constants_instance.__setattr__('DATETIME_FORMAT', "%m/%d/%Y")

    def test_constant_class_instance(self):
        """
        Test that the Constants class cannot be instantiated.
        """
        # Attempt to create an instance of Constants
        with self.assertRaises(TypeError):
            constants_instance = Constants()

if __name__ == '__main__':
    unittest.main()
