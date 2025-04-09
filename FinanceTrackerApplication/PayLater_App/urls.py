from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.payLaterDashboard,name='payLaterDashboard'),
    path('get-paylater-details/', views.getPayLaterDetails, name="getPayLaterDetails"),
    path('paylater-payment/', views.payLaterPayment, name="payLaterPayment"),
]
