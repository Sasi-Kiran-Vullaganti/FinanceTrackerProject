from typing import __all__
from rest_framework import serializers
from Transactions_App.models import Category,Subcategory,PaymentMethod

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_category_name(self, value):
        user = self.initial_data.get('user')
        if Category.objects.filter(user_id=user, category_name=value).exists():
            raise serializers.ValidationError("This category already exists for you!")
        return value

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['subcategory_id', 'subcategory_name', 'category']

class paymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['payment_method_id', 'payment_method_name', 'user','payment_type']