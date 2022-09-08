from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('craft/<int:craft_id>', views.get_craft, name='craft'),

]