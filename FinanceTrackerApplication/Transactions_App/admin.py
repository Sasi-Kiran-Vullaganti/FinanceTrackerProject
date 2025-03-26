from django.contrib import admin
from .models import Category, Subcategory, PaymentMethod, Transaction, Refund, PayLater

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "category_name", "user")
    search_fields = ("name", "user__username")

# Subcategory Admin
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("subcategory_id", "subcategory_name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

# Payment Method Admin
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("payment_method_id", "payment_method_name", "payment_type")
    list_filter = ("payment_type",)
    search_fields = ("name",)

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("txnid", "name", "amount", "type", "txn_date", "user")
    list_filter = ("type", "txn_date", "category", "payment_method")
    search_fields = ("name", "txnid", "user__username")
    ordering = ("-txn_date",)

# Refund Admin
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("refundid", "transaction", "amount", "mode", "refund_date", "refunded")
    list_filter = ("mode", "refund_date", "refunded")
    search_fields = ("refundid", "transaction__name")

# PayLater Admin
@admin.register(PayLater)
class PayLaterAdmin(admin.ModelAdmin):
    list_display = ("paylaterid", "transaction", "amount", "due_date", "paid")
    list_filter = ("due_date", "paid")
    search_fields = ("paylaterid", "transaction__name")
