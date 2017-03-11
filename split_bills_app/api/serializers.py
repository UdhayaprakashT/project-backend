from django.contrib.auth.models import User
from split_bills_app.models import Group, Bill, CustomUser

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    serializer class for user object
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')


class GroupSerializer(serializers.ModelSerializer):
    """
    serializer class for Pay group object
    """
    members = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'members')


class BillSerializer(serializers.ModelSerializer):
    """
    serializer class for Bill object
    """
    split_between = UserSerializer(many=True)
    paid_by = UserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Bill
        fields = ('id','name', 'paid_by','split_between','group','amount')
