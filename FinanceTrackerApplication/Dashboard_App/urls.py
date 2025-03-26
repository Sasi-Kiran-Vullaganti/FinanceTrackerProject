from django.urls import path
from . import views

urlpatterns = [
    path('',views.userDashboard,name='userDashboard'),
]
