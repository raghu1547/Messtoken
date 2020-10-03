from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'vendor'

urlpatterns = [
    path('dashboard/',token_list, name="dashboard"),
    path('order/',order, name="order"),
]
