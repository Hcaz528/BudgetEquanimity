from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from budget_app.models import Account, Budget
from budget_app.serializer import AccountSerializer, BudgetSerializer

import json
import traceback
# Create your views here.


def hello_world(request):
    # print(request)
    return render(request, 'budget_app/hello_world.html', {})


def NotFound404(request, resource=None):
    # print(request)
    print(resource)
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
    print('===========================')

    if request.method == 'POST':

        print('===========================\nRaw Data: "%s"' % request.body)
        request_object = json.loads(request.body)

        # for k, v in request_object.items():
        #     print(f'Key: {k}   |  Value: {v}')
        if "Premium" in request_object.keys():
            data["Premium"] = request_object["Premium"]
            return JsonResponse(data)
        else:
            data["Premium"] = "No peanuts can be found"
            return JsonResponse(data)

    return JsonResponse(data)


@api_view(['GET', 'POST', 'DELETE'])
def account_detail(request, pk):
    print('======================================')
    print('======================================')
    print('======================================')
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return JsonResponse({'message': 'This account does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    print('======================================')
    print('======================================')
    print('======================================')

    if request.method == 'GET':
        account_serializer = AccountSerializer(account)
        print(account_serializer)
        return JsonResponse(account_serializer.data)

    return JsonResponse({})


@api_view(['GET', 'POST', 'DELETE'])
def budget_detail(request, pk):
    print('======================================')
    print('======================================')
    print('======================================')
    try:
        budget = Budget.objects.get(pk=pk)
    except Budget.DoesNotExist:
        return JsonResponse({'message': 'This budget does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    print('======================================')
    print('======================================')
    print('======================================')

    if request.method == 'GET':
        budget_serializer = BudgetSerializer(budget)
        print(budget_serializer)
        return JsonResponse(budget_serializer.data)

    # TODO
    # - Set Up POST
    # - Set up DELETE
    # - Set up a DELETE Circumstance where if you wanted to start with a fresh budget it deletes that months budget an creates a fresh budget from last month's budget
    # NOTE

    return JsonResponse({})


@api_view(['GET', 'POST', 'DELETE'])
def budget_detail_filtered(request, pk, year, month):
    print('======================================')
    print('======================================')
    print('======================================')
    try:
        budget = Budget.objects.filter(pk=pk, budgets__year='2021')
    except Budget.DoesNotExist:
        return JsonResponse({'message': 'This budget does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
    print(budget.query)
    print(budget)
    print('======================================')
    print('======================================')
    print('======================================')

    if request.method == 'GET':
        # budget_serializer = BudgetSerializer(budget)
        # print(budget_serializer)
        # return JsonResponse(budget_serializer.data)
        return JsonResponse({})

    # TODO
    # - Set Up POST
    # - Set up DELETE
    # - Set up a DELETE Circumstance where if you wanted to start with a fresh budget it deletes that months budget an creates a fresh budget from last month's budget
    # NOTE

    return JsonResponse({})
