from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'vendor'


urlpatterns = [
    path('dashboard/', token_list, name='dashboard'),
    # path('revieworder/', order, name='revieworder'),
    path('pending/', pending, name='pending'),
    path('pending/<int:transid>', details, name="details"),


]
