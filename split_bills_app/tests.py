"""
Test Cases for the Split Bills App
"""
import unittest
from django.test.client import Client
from .models import CustomUser, Bill, Group


class APITest(unittest.TestCase):
    """
    Includes the test for the split_bills app
    """

    def setUp(self):
        """
        Initial Setup
        creates a user and logs the user in.
        """
        self.client = Client()

    def test_users_api(self):
        """
         Assert when users api returns success
        """
        udhay = CustomUser.objects.create(username="udhay", password="pass")
        prakash = CustomUser.objects.create(username="prakash", password="pass")
        response = self.client.get("/api/users/")
        print("USER", response.content)
        self.assertEquals(response.status_code, 200)

    def test_groups_api(self):
        """
         Assert when groups api returns success
        """
        udhay1 = CustomUser.objects.create(username="udhay1", password="pass")
        prakash1 = CustomUser.objects.create(username="prakash1", password="pass")
        group = Group.objects.create(name="test")
        group.members.add(udhay1)
        group.members.add(prakash1)
        group.save()
        response = self.client.get("/api/groups/")
        print("GROUP", response.content)
        self.assertEquals(response.status_code, 200)

    def test_bills_api(self):
        """
         Assert when bills api returns success
        """
        udhay2 = CustomUser.objects.create(username="udhay2", password="pass")
        prakash2 = CustomUser.objects.create(username="prakash2", password="pass")
        group = Group.objects.create(name="testgroup")
        group.members.add(udhay2)
        group.members.add(prakash2)
        group.save()
        bill = Bill.objects.create(name="test", group=group, paid_by=udhay2, amount=1000)
        bill.split_between.add(udhay2)
        bill.split_between.add(prakash2)
        bill.save()
        response = self.client.get("/api/bills/")
        print("BILL", response.content)
        self.assertEquals(response.status_code, 200)


