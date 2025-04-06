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

@api_view(['POST'])
def createCategory(request):
    user_id = request.data.get('user')
    category_name = request.data.get('category_name')

    # Check if Category already exists for this user
    if Category.objects.filter(user_id=user_id, category_name=category_name).exists():
        return Response(
            {"detail": "Category already exists for this user."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If invalid data - send serializer errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def createSubCategory(request):
    category_id = request.data.get('category')   # Pass category_id from frontend
    subcategory_name = request.data.get('subcategory_name')

    # Check if SubCategory already exists for the given category
    if Subcategory.objects.filter(category_id=category_id, subcategory_name=subcategory_name).exists():
        return Response({"detail": "SubCategory already exists for this category."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SubCategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createPaymentMethod(request):
    user_id = request.data.get('user')
    payment_method_name = request.data.get('payment_method_name')
    payment_type = request.data.get('payment_type')
    if PaymentMethod.objects.filter(user_id=user_id, payment_method_name__iexact=payment_method_name).exists():
        return Response({"detail": "Payment method already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = paymentMethodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)