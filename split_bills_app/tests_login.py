"""
Test Case for login for the Split Bills App
"""
import json
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from .models import CustomUser, Bill, Group

# Create your tests here.
class LoginTest(unittest.TestCase):
    """
    Includes the test for the split_bills app
    """

    def setUp(self):
        """
        Initial Setup
        creates a user and logs the user in.
        """
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@test.com", "hasher123")

    def test_login(self):
        """
        Asserts the status code from secure view
        """
        status = self.client.login(username='testuser', password='hasher123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(status)
        self.client.logout()

    def test_login_fail(self):
        """
        Assert status code and login status with wrong password login
        """
        status = self.client.login(username='testuser', password='hasher1234')
        response = self.client.get(reverse('index'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(status)


    def tearDown(self):
        """
        Remove the users from database after each test case
        """
        testuser = User.objects.get(username='testuser')
        testuser.delete()
