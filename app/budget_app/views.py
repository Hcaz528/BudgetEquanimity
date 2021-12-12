import logging
import traceback
import json
from budget_app.serializer import AccountSerializer, BudgetSerializer, BudgetSerializer_mini
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework import status

from budget_app.models import Account, Budget
from budget_app.tools import tools
from budget_app.JSONModels import business, everyday, investment, get_outer_shell

# TODO Time shenanigans
# from datetime import datetime

# now = datetime.now()

# current_time = now.strftime("%B")
# print("Current Time =", current_time)


# load my random JSONModels
# 'called': lambda **kwargs: caller(**kwargs),
tools['business'] = lambda **kwargs: business(**kwargs)
tools['everyday'] = lambda **kwargs: everyday(**kwargs)
tools['investment'] = lambda **kwargs: investment(**kwargs)


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

    # TODO create default template
    # Template
    # 1. Fresh
    # 2. Copied Over from last month
    # Catgories
    # Income -- Forever Category
    # Giving
    # Savings
    # Housing
    # Transportation
    # Food
    # Personal
    # Lifestyle
    # Health
    # Insurance
    # Debt -- Forever Category

    #############################################
    #######      POST METHOD START    ###########
    #############################################

    # If a method is posted it:
    #  1. creates/modifies a yaer
    #  2. creates/modifies a month

    if request.method == 'POST':
        logging.info(f'{request.method} request to URL path')

        template = None
        request_object = json.loads(request.body)
        logging.debug(request_object)
        logging.debug(request_object['template'])

        if request_object['template'] == "FRESH":
            template = get_outer_shell()
            inner_shell = tools['everyday'](
                path="inner_shell_everyday_month_default.json")

            # Cycle template looking for correct type
            for count, item in enumerate(template['budgets']):
                print(item, count)
                if item['type'].lower() == request_object['type'].lower():
                    template['budgets'][count]['month'][f"{months[request_object['month']-1]}"] = inner_shell
                    break
            # template[f"{request_object['type']}"] = inner_shell
            # f"{request_object['month']}"
            # template[f'{request_object['type']}'] = inner_shell f"{request_object['month']}"
            logging.debug("=========================================")
            logging.debug("template=============")
            logging.debug(template)

        # Month Area
        # ------------
        # TODO Create new Month budget
        # Create February first
        if month is not None:
            # What things can be updated/ created in the month's budget field(?)

            try:
                pass
            except BaseException as err:
                error_response = f"Unexpected {err=}, {type(err)=}"

                logging.debug(error_response)

        # Year Area
        # ------------
        # TODO Create new Year budget
        if month is None:
            pass

    #############################################
    #######      POST METHOD END      ###########
    #############################################

    #############################################
    ########      GET METHOD START    ###########
    #############################################
    if request.method == 'GET':
        # TODO check the requests for the type of budget it wants returned ==> Everyday:0, Business: 1, Investments:2

        logging.info(f'{request.method} request to URL path')
        # Query Buidling
        try:
            if month is None:
                query = f'''SELECT budget_id, budgets FROM budgets WHERE (CAST(budgets -> 'year' AS INTEGER) = {year} AND budget_id = {pk})'''
            else:
                query = f'''SELECT budget_id, budgets #>'{{budgets,0, month, {months[month-1]}}}' AS budgets
                FROM budgets
                WHERE (CAST(budgets -> 'year' AS INTEGER) = {year}
                AND budgets #>'{{budgets,0, month}}' ? '{months[month-1]}' = true
                AND budget_id = {pk})
                '''
        except IndexError:
            return JsonResponse({'message': 'There is no 13th month'},
                                status=status.HTTP_404_NOT_FOUND)

        try:
            budget = Budget.objects.raw(query)
            response_data = next(b for b in budget)
            logging.debug(response_data)
        except Budget.DoesNotExist:
            return JsonResponse({'message': 'This budget does not exist'},
                                status=status.HTTP_404_NOT_FOUND)
        except BaseException as err:
            error_response = f"Unexpected {err=}, {type(err)=}"

            logging.debug(error_response)
            logging.debug(budget.query)

            if(str(type(err)) == "<class 'StopIteration'>"):
                logging.debug(
                    f"Error most likely stemming from an empty response.\nQuery most likely contains a year or month not yet created for this user\nMonth: {months[month-1]}  |  Year: {year}")
                return JsonResponse({"error": error_response},
                                    status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"error": error_response},
                                status=status.HTTP_404_NOT_FOUND)

        logging.debug('======================================')
        logging.debug('======================================')
        logging.debug('======================================')
        logging.debug(budget)
        logging.debug('======================================')
        logging.debug('======================================')
        logging.debug('======================================')

        budget_serializer = BudgetSerializer_mini(response_data)  # Method 2 -
        logging.info(budget_serializer)
        return JsonResponse(budget_serializer.data)

    #############################################
    ########      GET METHOD END      ###########
    #############################################

    # TODO
    # - Set Up POST
    # - Set up DELETE
    # - Set up a DELETE Circumstance where if you wanted to start with a fresh budget it deletes that months budget an creates a fresh budget from last month's budget
    # NOTE

    return JsonResponse({})
