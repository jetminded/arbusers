from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    """
        Возвращает страницу о нас
        :param request: запрос
        :return: about_us.html
    """
    if request.method == "GET":
        return render(request, 'index.html')
    return redirect('/error')


def vineyards(request):
    """
        Возвращает страницу о виноградниках
        :param request: запрос
        :return: vineyards.html
    """
    if request.method == "GET":
        return render(request, 'vineyards.html')
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
