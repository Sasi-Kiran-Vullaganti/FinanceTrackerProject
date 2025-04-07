from typing import __all__
from rest_framework import serializers
from Transactions_App.models import Category,Subcategory,PaymentMethod

# ------------------ Category Serializer ------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_category_name(self, value):
        user = self.initial_data.get('user')  # Expecting user_id from request data
        value = value.strip()

        # Length Validation
        if len(value) < 3 or len(value) > 12:
            raise serializers.ValidationError("Category name must be between 3 and 12 characters.")

        # Alphabets with spaces only
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Category name should only contain alphabets and spaces.")

        # Duplicate Check
        if Category.objects.filter(user_id=user, category_name__iexact=value).exists():
            raise serializers.ValidationError("This category already exists for you!")

        return value.title()


# ------------------ SubCategory Serializer ------------------
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['subcategory_id', 'subcategory_name', 'category']

    def validate_subcategory_name(self, value):
        category = self.initial_data.get('category')  # Expecting category_id from request data
        value = value.strip()

        if len(value) < 3 or len(value) > 12:
            raise serializers.ValidationError("SubCategory name must be between 3 and 12 characters.")

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("SubCategory name should only contain alphabets and spaces.")

        if Subcategory.objects.filter(category_id=category, subcategory_name__iexact=value).exists():
            raise serializers.ValidationError("SubCategory already exists for this category.")

        return value.title()


# ------------------ Payment Method Serializer ------------------
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['payment_method_id', 'payment_method_name', 'user', 'payment_type']

    def validate_payment_method_name(self, value):
        user = self.initial_data.get('user')  # Expecting user_id from request data
        value = value.strip()

        if len(value) < 3 or len(value) > 12:
            raise serializers.ValidationError("Payment Method name must be between 3 and 12 characters.")

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Payment Method name should only contain alphabets and spaces.")

        if PaymentMethod.objects.filter(user_id=user, payment_method_name__iexact=value).exists():
            raise serializers.ValidationError("Payment Method already exists for this user.")

        return value.title()