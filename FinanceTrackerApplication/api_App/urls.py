from django.urls import path
from . import views

urlpatterns = [
    path('categories/add/',views.createCategory,name='createCategory'),
    path('subCategories/add/',views.createSubCategory,name='createSubCategory'),
    path('paymentMethods/add/', views.createPaymentMethod, name='createPaymentMethod'),
    path('categories/<str:pk>/',views.getAllCategories,name='getAllCategories'),
    path('subCategories/<int:pk>/',views.getAllSubCategories,name='getAllSubCategories'),
    path('paymentMethods/<str:pk>/',views.getAllPaymentMethod,name='getAllPaymentMethod'),
]