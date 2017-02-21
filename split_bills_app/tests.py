"""
Test Cases for the Split Bills App
"""
import json
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client

# Create your tests here.
class DebtDetailsTest(unittest.TestCase):
    """
    Includes the test for the split_bills app
    """

    def setUp(self):
        """
        Initial Setup
        gets the response for the get_debt_details view and stores in self.data
        """
        url = reverse("simplify-debts")
        self.client = Client()
        response = self.client.get(url)
        self.data = json.loads(response.content.decode("utf-8"))

    def test_total_debt(self):
        """
        Asserts the total debt for the users
        """
        self.assertEquals(self.data["Alice"]["total_debt"], 900)
        self.assertEquals(self.data["Bob"]["total_debt"], -900)
        self.assertEquals(self.data["Chris"]["total_debt"], 0)
