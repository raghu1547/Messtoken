from django.urls import path
from django.contrib.auth import views as auth_views
from .views import userlist, placeOrder
app_name = 'student'

urlpatterns = [
    path('dashboard/',userlist,name='dashboard'),
    path('placeorder/',placeOrder, name='placeOrder')
]