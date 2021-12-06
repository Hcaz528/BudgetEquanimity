from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

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
