from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = "customusers"
        verbose_name_plural = "CustomUsers"

    def __str__(self):
        return str(self.username)

class Group(models.Model):
    """
    group table to store groups
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200, null=True)
    members = models.ManyToManyField(User)

    class Meta:
        db_table = "groups"
        verbose_name_plural = "Groups"

    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    """
    bills table to store bills
    """
    name = models.CharField(max_length=30)
    paid_by = models.ForeignKey(User, related_name='bill_paid_by', on_delete=models.CASCADE)
    split_between = models.ManyToManyField(User)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bills"
        verbose_name_plural = "Bills"

    def __str__(self):
        return str(self.name)
