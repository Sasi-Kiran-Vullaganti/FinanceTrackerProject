from django.urls import path
from . import views

urlpatterns = [
    path('categories/<str:pk>',views.getAllCategories,name='getAllCategories'),
    path('subCategories/<int:pk>',views.getAllSubCategories,name='getAllSubCategories'),
    path('paymentMethods/<str:pk>',views.getAllPaymentMethod,name='getAllPaymentMethod'),
]