from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.refundsDashboard,name='refundsDashboard'),
]
