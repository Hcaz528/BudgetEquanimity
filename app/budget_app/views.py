from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework import status

from budget_app.models import Account, Budget
from budget_app.serializer import AccountSerializer, BudgetSerializer, BudgetSerializer_mini

import json
import traceback
import logging

level = logging.DEBUG
fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)
# Create your views here.


def hello_world(request):
    # logging.info(request)
    return render(request, 'budget_app/hello_world.html', {})


def NotFound404(request, resource=None):
    # logging.info(request)
    logging.info(resource)
    return render(request, 'budget_app/404.html', {"resource": resource})


def goodbye_world(request):
    return render(request, 'budget_app/goodbye_world.html', {})


@api_view(['GET', 'POST', 'DELETE'])
def test_sql_query(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    logging.debug('===========================')

    if request.method == 'POST':

        logging.debug('===========================\nRaw Data: "%s"' %
                      request.body)
        request_object = json.loads(request.body)

        # for k, v in request_object.items():
        #     logging.debug(f'Key: {k}   |  Value: {v}')
        if "Premium" in request_object.keys():
            data["Premium"] = request_object["Premium"]
            return JsonResponse(data)
        else:
            data["Premium"] = "No peanuts can be found"
            return JsonResponse(data)

    return JsonResponse(data)


@api_view(['GET', 'POST', 'DELETE'])
def account_detail(request, pk):
    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return JsonResponse({'message': 'This account does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')

    if request.method == 'GET':
        account_serializer = AccountSerializer(account)
        logging.info(account_serializer)
        return JsonResponse(account_serializer.data)

    return JsonResponse({})


@api_view(['GET', 'POST', 'DELETE'])
def budget_detail(request, pk):
    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')
    try:
        budget = Budget.objects.get(pk=pk)
    except Budget.DoesNotExist:
        return JsonResponse({'message': 'This budget does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')

    if request.method == 'GET':
        # logging.debug(budget.budgets)
        budget_serializer = BudgetSerializer(budget)
        logging.info(budget_serializer)
        return JsonResponse(budget_serializer.data)

    # TODO
    # - Set Up POST
    # - Set up DELETE
    # - Set up a DELETE Circumstance where if you wanted to start with a fresh budget it deletes that months budget an creates a fresh budget from last month's budget
    # NOTE

    return JsonResponse({})


@api_view(['GET', 'POST', 'DELETE'])
def budget_detail_filtered(request, pk, year, month=None):
    # NOTE Raw Queries must include the primary key
    # NOTE very helpful --> # print(dir(next(<RawQuerySet>.iterator())))
    # NOTE There are two methods(hacks that are essentially the same) for handling the RawQuerySet in Django
    # HACK 1: Create a generator by calling the iterator method and then wrap the result in a next() function
    # HACK 2: Create a for loop generator [b for b in <RawQuerySet>] and then wrap that in a next() funciton
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    # Query Buidling
    if month is None:
        query = f'''SELECT budget_id, budgets FROM budgets WHERE (CAST(budgets -> 'year' AS INTEGER) = {year} AND budget_id = {pk})'''
    else:
        query = f'''SELECT budget_id, budgets FROM budgets
        WHERE (CAST(budgets -> 'year' AS INTEGER) = {year}
		AND budgets #>'{{budgets,0, month}}' ? '{months[month+1]}' = true
        AND budget_id = {pk})
        '''

    try:
        budget = Budget.objects.raw(query)

    except Budget.DoesNotExist:
        return JsonResponse({'message': 'This budget does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    # TODO Handle when a month is not present in the RawQuerySet
    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug(budget)
    logging.debug('======================================')
    logging.debug('======================================')
    logging.debug('======================================')

    if request.method == 'GET':
        budget_serializer = BudgetSerializer_mini(
            next(b for b in budget))  # Method 2 -
        logging.info(budget_serializer)
        return JsonResponse(budget_serializer.data)

    # TODO
    # - Set Up POST
    # - Set up DELETE
    # - Set up a DELETE Circumstance where if you wanted to start with a fresh budget it deletes that months budget an creates a fresh budget from last month's budget
    # NOTE

    return JsonResponse({})
