from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.userDashboard,name='userDashboard'),
    path('',views.defaultRedirection,name='defaultRedirection')
]
