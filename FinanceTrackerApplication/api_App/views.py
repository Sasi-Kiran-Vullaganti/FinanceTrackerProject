from django.shortcuts import render
from Transactions_App.models import Category,Subcategory,PaymentMethod
from userModule_App.models import UserProfile
from rest_framework.decorators import api_view
from .serializers import CategorySerializer,SubCategorySerializer,PaymentMethodSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def getAllCategories(request, pk):
    user = get_object_or_404(UserProfile, userid=pk)
    categories = Category.objects.filter(user=user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getAllSubCategories(request, pk):
    category = get_object_or_404(Category, category_id=pk)
    subCategories = Subcategory.objects.filter(category=category)
    serializer = SubCategorySerializer(subCategories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getAllPaymentMethod(request, pk):
    user = get_object_or_404(UserProfile, userid=pk)
    
    # Get the transaction type from query parameters
    payment_type = request.query_params.get('payment_type', None)
    
    # Filter payment methods based on user and optional payment type
    if payment_type:
        payments = PaymentMethod.objects.filter(user=user, payment_type=payment_type)
    else:
        payments = PaymentMethod.objects.filter(user=user)
    
    serializer = PaymentMethodSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createCategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createSubCategory(request):
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createPaymentMethod(request):
    serializer = PaymentMethodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)