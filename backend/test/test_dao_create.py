import pytest

from jsonschema import validate
from unittest.mock import patch
from unittest import TestCase

from src.util.validators import getValidator

class TestDAOCreate(TestCase):
    @pytest.fixture(autouse=True)
    def sut(self):
        with patch('src.util.dao.DAO', autospec=True) as mockedDAO:
            self.mockedDAO = mockedDAO
            mockedDAO.return_value = None
            def prepMock(collection, data):
                try:
                    validate(instance=data, schema=getValidator(collection)["$jsonSchema"])
                    mockedDAO.create.return_value = data
                except Exception as e:
                    mockedDAO.create.side_effect = e

            self.prepMock = prepMock

    @pytest.mark.integration
    def test_create_valid_task(self):
        """
        Tests that no Expection is raised when valid task is created.
        """
        collection = "task"
        testData = {'title': 'Test', 'description': 'Test'}
        self.prepMock(collection, testData)
        try:
            self.mockedDAO.create(testData)
        except Exception:
            self.fail("Valid task not recognized as valid.")
        
    
    @pytest.mark.integration
    def test_create_not_valid_task(self):
        """
        Tests that a Expection is raised when not valid task is created.
        """
        collection = "task"
        testData = {'title': 'Test'}
        self.prepMock(collection, testData)
        self.assertRaises(Exception, self.mockedDAO.create, testData)
    
    @pytest.mark.integration
    def test_create_valid_todo(self):
        """
        Tests that no Expection is raised when valid todo is created.
        """
        collection = "todo"
        testData = {'description': 'Test', 'done': False}
        self.prepMock(collection, testData)
        try:
            self.mockedDAO.create(testData)
        except Exception:
            self.fail("Valid todo not recognized as valid.")
    
    @pytest.mark.integration
    def test_create_not_valid_todo(self):
        """
        Tests that a Expection is raised when not valid todo is created.
        """
        collection = "todo"
        testData = {'done': True}
        self.prepMock(collection, testData)
        self.assertRaises(Exception, self.mockedDAO.create, testData)
    
    @pytest.mark.integration
    def test_create_valid_user(self):
        """
        Tests that no Expection is raised when valid user is created.
        """
        collection = "user"
        testData = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test@test.com'}
        self.prepMock(collection, testData)
        try:
            self.mockedDAO.create(testData)
        except Exception:
            self.fail("Valid user not recognized as valid.")
    
    @pytest.mark.integration
    def test_create_not_valid_user(self):
        """
        Tests that a Expection is raised when not valid user is created.
        """
        collection = "user"
        testData = {'firstName': 'Test', 'lastName': 'Test'}
        self.prepMock(collection, testData)
        self.assertRaises(Exception, self.mockedDAO.create, testData)
    
    @pytest.mark.integration
    def test_create_valid_video(self):
        """
        Tests that no Expection is raised when valid video is created.
        """
        collection = "video"
        testData = {'url': 'https://www.youtube.com/watch?v=5rz1TcLVFzY'}
        self.prepMock(collection, testData)
        try:
            self.mockedDAO.create(testData)
        except Exception:
            self.fail("Valid video not recognized as valid.")
    
    @pytest.mark.integration
    def test_create_not_valid_video(self):
        """
        Tests that a Expection is raised when not valid video is created.
        """
        collection = "video"
        testData = {'name': 'Test Video'}
        self.prepMock(collection, testData)
        self.assertRaises(Exception, self.mockedDAO.create, testData)
        