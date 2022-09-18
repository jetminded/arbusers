import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from predictions import find_closest

def index(request):
    """
        Возвращает страницу о нас
        :param request: запрос
        :return: about_us.html
    """
    if request.method == "GET":
        return render(request, 'index.html')
    return redirect('/error')


def get_database(request):
    data_list = []
    existing_vineyards = ExistingVineyard.objects.all()
    for v in existing_vineyards:
        vineyard_info = {
            "id": v.id,
            "x": v.x,
            "y": v.y,
            "name": v.name,
            "grape": v.grape,
        }
        data_list.append(vineyard_info)
    print(data_list)
    return JsonResponse({'success': True, 'data': data_list})


@csrf_exempt
def vineyards(request):
    """
        Возвращает страницу о виноградниках
        :param request: запрос
        :return: vineyards.html
    """
    if request.method == "GET":
        return render(request, 'vineyards.html')

    if request.method == "POST":
        data = json.loads(request.POST.get('chosen_vineyards'))
        vineyard_x = []
        vineyard_y = []
        for id in data.keys():
            vineyard = ExistingVineyard.objects.get(id=id)
            vineyard_x.append(vineyard.x)
            vineyard_y.append(vineyard.y)
            result = find_closest(vineyard_x, vineyard_y, len(vineyard))
        # process data.keys()
        return HttpResponse(str(data.keys()))
    return redirect('/error')


def about_us(request):
    """
    Возвращает страницу о нас
    :param request: запрос
    :return: about_us.html
    """
    if request.method == "GET":
        return render(request, 'about_us.html')
    return redirect('/error')


def error(request):
    """
        Возвращает страницу ошибки
        :param request: запрос
        :return: error.html
    """
    return HttpResponse("error 404")
