from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('vineyards/', vineyards, name='vineyards'),
    path('about_us/', about_us, name='about_us'),
    path('error/', error, name='error'),
    path('vineyards/get_database/', get_database, name='get_database'),
]
