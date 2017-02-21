"""
Test Case for login for the Split Bills App
"""
import json
import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from .models import PayGroup, Bill
from django.contrib.auth.models import User

# Create your tests here.
class LoginTest(unittest.TestCase):
    """
    Includes the test for the split_bills app
    """

    def setUp(self):
        """
        Initial Setup
        creates a few users (members) and create group object and bill object.

        """
        joe = User.objects.create_user("joe", "joe@test.com", "joe123")
        mike = User.objects.create_user("mike", "mike@test.com", "mike123")
        doe = User.objects.create_user("doe", "doe@test.com", "doe123")
        group = PayGroup(name='Foodies')
        group.save()
        group.members.add(joe)
        group.members.add(mike)
        group.members.add(doe)

        bill = Bill(name='Dinner', paid_by=mike, group=group, amount=9000)
        bill.save()
        bill.split_between.add(joe)
        bill.split_between.add(mike)
        bill.split_between.add(doe)


    def test_group(self):
        """
        Asserts the group name and member names
        """
        foodies = PayGroup.objects.get(name='Foodies')
        members = foodies.members.all()
        self.assertEqual(foodies.name, 'Foodies')
        self.assertEqual(members[0].username, 'joe')
        self.assertEqual(members[1].username, 'mike')
        self.assertEqual(members[2].username, 'doe')

    def test_bill(self):
        """
        Asserts the status code from secure view
        """
        bill = Bill.objects.get(name='Dinner')
        split_between = bill.split_between.all()
        self.assertEqual(bill.name, 'Dinner')
        self.assertEqual(split_between[0].username, 'joe')
        self.assertEqual(split_between[1].username, 'mike')
        self.assertEqual(split_between[2].username, 'doe')
        self.assertEqual(bill.paid_by.username, 'mike')
        self.assertEqual(bill.group.name, 'Foodies')

    def tearDown(self):
        """
        Remove the users from database after each test case
        Remove the group from database after each test case
        Remove the bill from database after each test case
        """
        User.objects.all().delete()
        PayGroup.objects.all().delete()
        Bill.objects.all().delete()
