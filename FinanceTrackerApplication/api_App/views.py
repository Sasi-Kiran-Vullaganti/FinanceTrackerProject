from django.shortcuts import render
from Transactions_App.models import Category,Subcategory,PaymentMethod
from userModule_App.models import UserProfile
from rest_framework.decorators import api_view
from .serializers import CategorySerializer,SubCategorySerializer,paymentMethodSerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def getAllCategories(request,pk):
    try:
        user = UserProfile.objects.get(userid=pk)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    categories = Category.objects.filter(user=user)
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllSubCategories(request,pk):
    try:
        category = Category.objects.get(category_id=pk)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    subCategories = Subcategory.objects.filter(category_id=category)
    serializer = SubCategorySerializer(subCategories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllPaymentMethod(request,pk):
    try:
        user = UserProfile.objects.get(userid=pk)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    payments = PaymentMethod.objects.filter(user=user)
    serializer = paymentMethodSerializer(payments,many=True)
    return Response(serializer.data)