from django.urls import path
from django.contrib.auth import views as auth_views
from .views import userlist, order, pending, details
app_name = 'student'

urlpatterns = [
    path('dashboard/', userlist, name='dashboard'),
    path('placeorder/', order, name='placeorder'),
    path('pending/', pending, name='pending'),
    path('pending/<int:transid>', details, name="details"),


]
