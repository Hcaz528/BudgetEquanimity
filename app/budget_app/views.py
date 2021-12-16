import logging
import traceback
import json
from budget_app.serializer import AccountSerializer, BudgetSerializer, BudgetSerializer_mini, BudgetSerializer_new
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework import status

from budget_app.models import Account, Budget
from budget_app.tools import tools
from budget_app.JSONModels import business, everyday, investment, get_outer_shell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
fmt = bcolors.FAIL+'[%(levelname)s]    '+bcolors.ENDC + \
    bcolors.WARNING+'%(asctime)s - %(message)s'+bcolors.ENDC
# fmt = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=fmt)
# Create your views here.


def decompose_next(generator):
    return next((g for g in generator), None)


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

    # TODO Overwrite a month

    #############################################
    #######      POST METHOD START    ###########
    #############################################

    # If a method is posted it:
    #  1. creates/modifies a yaer
    #  2. creates/modifies a month

    if request.method == 'POST':

        logging.info(f'{request.method} request to URL path')
        template = None  # Outer Template
        template_for_requested_year = None
        current_template = None
        request_object = json.loads(request.body)
        # TODO build this out
        # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

        # Create a function that makes the outside shell of the json    |   Either fresh or from DB
        def outer_shell():
            # fresh
            # from db
            pass

        # Create a function that makes the inside  shell of the json    |   Either fresh or from DB
        def inner_shell():
            # fresh
            # from db
            pass

        # Have functions assimilate with each other once the appropriate data has been created or found
        def shell_assimilation():
            pass

        # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

        logging.debug(request_object)
        logging.debug(request_object['template'])

        # Check to see if there is a budget for the target year
        # If a budget doesn't already exist for the target year then a fresh one will be made
        try:
            # Find the target year from DB
            logging.debug("=====================querying db")
            budget = Budget.objects.raw(
                f'''SELECT budget_id, year FROM budgets WHERE to_char(year, 'YYYY')::integer = {request_object['year']}''')
            logging.debug(budget.query)
            logging.debug("=====================querying db")

            # Extract data from the generator object
            # Check to see it the iterator has a next, if not return None
            response_data = decompose_next(budget)
            logging.debug("=====================response_data")

            # Check that there is data from the query
            # Make/ Find Budget for target year
            if response_data is not None:
                template_for_requested_year = getattr(response_data, 'year')
                current_template = getattr(response_data, 'budgets')
            else:
                logging.debug(
                    '\n\nNo budgets; Create New budget for this year\n\n\n')
            template = get_outer_shell() if current_template is None else current_template
            template['year'] = request_object['year']
            logging.debug("=====================response_data")

        except BaseException as err:
            error_response = f"Unexpected {err=}, {type(err)=}"

        # TODO If it is not going to be a fresh template load the template from last month and substitute in in for next month/ year-month
        # if request_object['template'] == "FromLast":
        #     template = READ DATABASE

        if request_object['template'] == "FRESH" and current_template is None:
            # Below code results in:
            #         inner_shell = tools["everyday"](path="inner_shell_everyday_month_default.json")
            # OR      inner_shell = tools["business"]()
            # OR      inner_shell = tools["investment"]()

            # Cycle template looking for correct type
            for count, item in enumerate(template['budgets']):
                if item['type'].lower() == request_object['type'].lower():
                    # Below code results in something like:
                    #         template['budgets'][0]['month']['March'] = inner_shell
                    logging.debug(
                        f"\n{template['budgets'][count]['month']}\n")
                    target_month = f"{months[request_object['month']-1]}"
                    if target_month in template['budgets'][count]['month']:
                        logging.debug(
                            f"{request_object['month']} was already present in {request_object['year']}")
                        break
                    else:
                        inner_shell = tools[request_object['type'].lower()](
                            path="inner_shell_everyday_month_default.json")
                        template['budgets'][count]['month'][f"{target_month}"] = inner_shell
                    break
            logging.debug("=========================================")
            # logging.debug(request.POST['year'])
            logging.debug("template=============")

            logging.debug(template)
            # current_template = None
            budget_dos = Budget.objects.get(pk=pk)
            budget_serializer = BudgetSerializer_new(budget_dos, data={"year": request_object['year'],
                                                     "type": request_object['type'],
                                                                       "budgets": template})
            logging.info(budget_serializer)
            if budget_serializer.is_valid():
                budget_serializer.save()
                return JsonResponse({"method": request.method,
                                     "response": "Updated",
                                     "template_type": request_object['template'],
                                     "data": template,
                                     "Status": f"There was already data in {str(request_object['month'])+'/'+str(request_object['year'])}"})
        elif current_template is not None:
            return JsonResponse({"method": request.method,
                                 "response": "Updated",
                                 "template_type": request_object['template'],
                                 "data": None,
                                 "Status": f"There was already data in {str(request_object['month'])+'/'+str(request_object['year'])}"})

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

        return JsonResponse({"method": request.method, "response": "Updated"})

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
            return JsonResponse({'message': 'There is no 13th, 14th, or nth month that is not between 1 - 12'},
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
