import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .predictions import *

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

    return JsonResponse({'success': True, 'data': data_list})


@csrf_exempt
def vineyards(request):
    """
        Возвращает страницу о виноградниках
        :param request: запрос
        :return: vineyards.html
    """
    if request.method == "GET":
        return render(request, 'vineyards.html', {'data': json.dumps({}), 'result': json.dumps({'center': [], 'left': [], 'right': []})})
    if request.method == "POST":
        data = json.loads(request.POST.get('chosen_vineyards'))
        vineyard_x = []
        vineyard_y = []
        for id in data.keys():
            vineyard = ExistingVineyard.objects.get(id=id)
            vineyard_x.append(int(abs(vineyard.x_abs - x_base)/100))
            vineyard_y.append(int(abs(y_base - vineyard.y_abs)/100))
        dict_result = find_closest(vineyard_x, vineyard_y, 10)
        center = list(zip(dict_result["x_center"], dict_result["y_center"]))
        left = list(zip(dict_result["x_left"], dict_result["y_bottom"]))
        right = list(zip(dict_result["x_right"], dict_result["y_top"]))

        center = [from_picture_to_map(item) for item in center]
        left = [from_picture_to_map(item) for item in left]
        right = [from_picture_to_map(item) for item in right]
        # process data.keys()
        return render(request, 'vineyards.html', {'data': json.dumps(data), 'result': json.dumps({'center': center, 'left': left, 'right': right})})
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
