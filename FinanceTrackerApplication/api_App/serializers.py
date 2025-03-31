from typing import __all__
from rest_framework import serializers
from Transactions_App.models import Category,Subcategory,PaymentMethod

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'user']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['subcategory_id', 'subcategory_name', 'category']

class paymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['payment_method_id', 'payment_method_name', 'user','payment_type']