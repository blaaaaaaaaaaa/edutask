import pytest
from unittest.mock import MagicMock
from unittest import TestCase

from src.util.dao import DAO
from src.controllers.usercontroller import UserController

class TestEmailLogin(TestCase):
    @pytest.mark.unit
    def test_valid_email(self):
        """
        Tests that no ValueError is raised when valid email is used.
        """
        testUser = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test@test.com'}
        DAO.find = MagicMock(return_value=[testUser])
        userController = UserController(DAO)
        try:
            userController.get_user_by_email(testUser['email'])
        except ValueError:
            self.fail("Valid email not recognized as valid.")
    
    @pytest.mark.unit
    def test_not_valid_email(self):
        """
        Tests that an ValueError is raised when not valid email is used.
        """
        testUser = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test.test'}
        DAO.find = MagicMock(return_value=[testUser])
        userController = UserController(DAO)
        self.assertRaises(ValueError, userController.get_user_by_email, testUser['email'])

    @pytest.mark.unit
    def test_registered_email(self):
        """
        Tests that the correct user object is returned when registered email is used.
        """
        testUser = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test@test.com'}
        DAO.find = MagicMock(return_value=[testUser])
        userController = UserController(DAO)
        user = userController.get_user_by_email(testUser['email'])
        assert user == testUser
    
    @pytest.mark.unit
    def test_not_registered_email(self):
        """
        Tests that an Exception is raised when not registered email is used.
        """
        testUser = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test@test.com'}
        DAO.find = MagicMock(side_effect=Exception)
        userController = UserController(DAO)
        self.assertRaises(Exception, userController.get_user_by_email, testUser['email'])
    
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    @pytest.mark.unit
    def test_multiple_registered_email(self):
        """
        Tests that the correct user object is returned when registered email is used.
        Also tests that an Error is printed out.
        """
        testUser = {'firstName': 'Test', 'lastName': 'Test', 'email': 'test.test@test.com'}
        DAO.find = MagicMock(return_value=[testUser, testUser])
        userController = UserController(DAO)
        user = userController.get_user_by_email(testUser['email'])
        capturedPrint = self.capsys.readouterr()
        assert capturedPrint.out == 'Error: more than one user found with mail test.test@test.com\n'
        assert user == testUser
