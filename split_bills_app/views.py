"""
    Views for the Split Bills App
"""
import os
import json
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Bill, Group

# Create your views here.

@login_required()
def get_index_page(request):
    '''
    Returns the homepage
    '''
    return HttpResponse('Welcome To Django')


def simplify_debt(request):
    '''
    Return the debt details as a json in the following format:
    {
        "Alice": {
            "total_debt": 900,
            "individual_debt": {
                "Bob": 900,
                "Chris": 0
            }
        },

        "Bob": {
            "total_debt": -900,
            "individual_debt": {
                "Alice": -900,
                "Chris": 0
            }
        },

        "Chris": {
            "total_debt": 0
            "individual_debt": {
                "Alice": 0,
                "Bob": 0
            }
        }
    }

    A negative value assumes that the user has to give the amount
    and a positive values assumes that the user gets the amount

    According to the above example,
    data['Alice']['total_debt] = 1100 implies that Alice gets back 1100.
    data['Alice']['individual_debt']['Bob'] implies that Alice gets back 700 from Bob.
    data['Bob']['total_debt] = -700 implies that Bob has to give 700.
    data['Bob']['individual_debt']['Alice'] = -700 implies that Bob has to give 700 to Alice.
    '''

    #populate this dictionary with the response data to be returned

    data = {}

    # function to return person with minimum total_debts
    def min_get():
        min_index = min(data.items(), key=lambda d: (lambda k, v: float(v["total_debt"]))(*d))
        return min_index[0]

    # function to return person with maximum total_debts
    def max_get():
        max_index = max(data.items(), key=lambda d: (lambda k, v: float(v["total_debt"]))(*d))
        return max_index[0]

    # Recursive function calculates individual_debts
    def min_cash_rec():
        min_debt = min_get()
        max_debt = max_get()
        if (data[min_debt]["total_debt"] == 0 and data[max_debt]["total_debt"] == 0):
            return
        abs_min = min(-data[min_debt]["total_debt"], data[max_debt]["total_debt"])
        data[max_debt]["total_debt"] -= abs_min
        data[min_debt]["total_debt"] += abs_min
        data[max_debt]["individual_debt"][min_debt] = abs_min
        data[min_debt]["individual_debt"][max_debt] = -abs_min
        min_cash_rec()

    # loads the json data
    with open("split_bills_app/sample_expenditure.json") as json_data:
        d = json.load(json_data)

    # get all the users
    users = []
    for bills in d:
        for bill_key in bills:
            if bill_key == "paid_by":
                users.append(bills[bill_key])
            if bill_key == "split_between":
                for split_users in bills[bill_key]:
                    users.append(split_users)

    # retrieve unique users
    users = list(set(users))
    for user in users:
        data[user] = {
            "total_debt": 0,
            "individual_debt": {}
        }
        for other_user in [other_users for other_users in users if other_users != user]:
            data[user]["individual_debt"][other_user] = 0

    # calculate total debts of each person
    for bills in d:
        for bill_key in bills:
            if bill_key == "paid_by":
                data[bills[bill_key]]["total_debt"] += bills["total_bill_amount"]
            if bill_key == "split_between":
                for bill_split_users in bills[bill_key]:
                    data[bill_split_users]['total_debt'] -= bills['total_bill_amount'] / len(bills[bill_key])
    full_dept = {}

    # copy of total_depts as it will be modified and needed later
    for user in users:
        full_dept[user] = data[user]["total_debt"]

    # calling the function to calculate individual_debts
    min_cash_rec()

    # copying the original total_depts back after modification
    for user in users:
        data[user]["total_debt"] = full_dept[user]

    return HttpResponse(json.dumps(data), content_type='application/json')

