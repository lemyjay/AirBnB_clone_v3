#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.storage = DBStorage()

    def setUp(self):
        """Setup method"""
        # Create some test objects
        self.state = State()
        self.state.name = "California"
        self.state.save()

    def tearDown(self):
        """Teardown method"""
        # Clean up created objects
        os.remove("file.json")

    def test_get(self):
        """Test the get method"""
        obj = self.storage.get(State, self.state.id)
        self.assertEqual(obj, self.state)

        # Test getting non-existent object
        obj = self.storage.get(State, "non_existent_id")
        self.assertIsNone(obj)

    def test_count(self):
        """Test the count method"""
        # Test counting all objects
        count_all = self.storage.count()
        self.assertEqual(count_all, 1)

        # Test counting specific class objects
        count_state = self.storage.count(State)
        self.assertEqual(count_state, 1)

        # Create more test objects
        state2 = State()
        state2.name = "New York"
        state2.save()

        count_all_after = self.storage.count()
        count_state_after = self.storage.count(State)

        self.assertEqual(count_all_after, 2)
        self.assertEqual(count_state_after, 2)
