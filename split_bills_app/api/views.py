from split_bills_app.api import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from split_bills_app.models import Group, Bill, CustomUser
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        """
        Return all users
        """
        return User.objects.all()

    def create(self, request, *args):
        user = request.data
        new_user = User.objects.create(
            username=user.get("username","None")
        )
        new_user.set_password(user.get("password","None"))
        new_user.save()

class CustomUserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def create(self, request, *args):
        userdata = request.POST
        new_user = CustomUser(username=userdata.get("username","None"), password=userdata.get("password","None"))
        new_user.save()
        return HttpResponseRedirect('/api/users')

class GroupViewSet(viewsets.ModelViewSet):
    """
    group view set
    """
#     permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        """
        Filter groups based on logged in user
        """
        groups = []
        groupname = self.request.query_params.get('groupname', None)
        if groupname:
            groups = Group.objects.filter(name=groupname)
            if not groups:
                raise Exception("Group - {} name not valid".format(groupname))
        else:
            groups = Group.objects.all()
        return groups

    def create(self, request):
        """
        Get the members from db based on requested group member set
        Creat a Group
        Add members to the group
        """
        group = request.data
        users = []
        for i in group['members']:
            users.append(i['username'])
        members = User.objects.filter(username__in=users)
        new_group = Group(name=group['name'])
        new_group.save()
        for member in members:
            new_group.members.add(member)
            
    def update(self, request, *args, **kwargs):
        """
        Get the members from db based on requested group member set
        Creat a Group
        Add members to the group
        """
        req_data = request.data
        group_name = req_data.get("name", None)
        members = req_data.get("members", None)
        
        try:
            group = Group.objects.get(name=group_name)
        except Exception as ex:
            return Exception("Group name does not exits.")

        users = []
        for member in members:
            users.append(member['username'])
        group_members = User.objects.filter(username__in=users)

        group.members.clear()
        for member in group_members:
            group.members.add(member)

class BillViewSet(viewsets.ModelViewSet):
    """
    Bill view set
    """
#     permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BillSerializer

    def get_queryset(self):
        """
        Get bill based on query string group name
        """
        bills = []
        groupname = self.request.query_params.get('groupname', None)
        if groupname:
            try:
                group = Group.objects.get(name=groupname)
                bill = Bill.objects.filter(group=group)
            except Exception as ex:
                raise Exception(ex)
        else:
            bill = Bill.objects.all()
        return bill

    def create(self, request):
        """
        read bill name and other data from post data
        find group and paid_by user object
        Creat a bill
        """
        bill = request.data
        try:
            paid_by = User.objects.get(username=bill['paid_by']['username'])
        except Exception as ex:
            raise Exception("Paid by user - {} doesn't exists.".format(bill['paid_by']))

        split_between = []
        for i in bill['split_between']:
            split_between.append(i['username'])

        users = User.objects.filter(username__in=split_between)

        try:
            group = Group.objects.get(name=bill['group']['name'])
        except Exception as ex:
            raise Exception("Bill group - {} doesn't exists.".format(bill['group']['name']))

        new_bill = Bill(name=bill['name'], paid_by=paid_by, group=group, amount=bill['amount'])
        new_bill.save()
        for user in users:
            new_bill.split_between.add(user)

    def update(self, request, *args, **kwargs):
        """
        Get the members from db based on requested group member set
        Creat a Group
        Add members to the group
        """
        bill = request.data
        name = bill.get("name", None)
        split_between = bill.get("split_between", None)
        group_name = bill.get("group", None)
        amount = bill.get("amount", None)
        object_id = request.data.get("id", None)

        if not split_between and  not group_name and  not amount and not name:
            raise Exception("split_between, group, amount and name are required parameter.")


        groups = Group.objects.filter(name=group_name["name"])

        if not groups:
            raise Exception("Group name does not exists.")
        group = groups[0]

        try:
            paid_by = User.objects.get(username=bill['paid_by']['username'])
        except Exception as ex:
            raise Exception("Paid by user doesn't exists.")

        try:
            bill = Bill.objects.get(id=object_id)
        except Exception as ex:
            raise Exception(ex)

        split_between = []
        for i in split_between:
            split_between.append(i['username'])
        members = User.objects.filter(username__in=split_between)
        bill.split_between.clear()

        for member in members:
            bill.split_between.add(member)

        bill.name = name
        bill.group = group
        bill.amount = amount
        bill.paid_by = paid_by
        bill.save()
