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
    group_bills = []
    
    group = Group.objects.get(name='Foodies')
    bills = Bill.objects.filter(group=group)
    for i in bills:
        bill = {}
        bill['paid_by'] = i.paid_by.username
        split_between = []
        for u in i.split_between.all():
            split_between.append(u.username)
        bill['split_between'] = split_between
        bill['total_bill_amount'] = i.amount
        group_bills.append(bill)
    payers = {}
    
    for bill in group_bills:
        payer = bill['paid_by']
        if not payer in payers:
            payers[payer] = {}
            if not 'individual_debt' in payers[payer]:
                payers[payer]['individual_debt'] = {}
            if not 'total_debts' in payers[payer]:
                payers[payer]['total_debt'] = 0
        split_number = len(bill['split_between'])
        debt = bill['total_bill_amount'] / split_number

        for member in bill['split_between']:
            if not member in payers:
                payers[member] = {}
                if not 'individual_debt' in payers[member]:
                    payers[member]['individual_debt'] = {}
                if not 'total_debts' in payers[member]:
                    payers[member]['total_debt'] = 0
            if payer != member:
                payers[member]['total_debt'] -= debt
                if not member in payers[payer]['individual_debt']:
                    payers[payer]['individual_debt'][member] = 0
                if not payer in payers[member]['individual_debt']:
                    payers[member]['individual_debt'][payer] = 0
                payers[payer]['individual_debt'][member] += debt
            else:
                payers[payer]['total_debt'] += debt * (split_number - 1)
    return HttpResponse(json.dumps(payers), content_type='application/json')
