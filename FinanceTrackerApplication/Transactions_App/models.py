from django.db import models
from userModule_App.models import UserProfile
import uuid


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'category_name')  
        ordering = ['category_name']  

    def __str__(self):
        return self.category_name



class Subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subcategory_name} (Category: {self.category.category_name})"


class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]
    payment_method_id = models.AutoField(primary_key=True)
    payment_method_name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="payment_methods")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'payment_method_name')

    def __str__(self):
        return f"{self.payment_method_name} ({self.payment_type}) - {self.user.name}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    EXPENSE_TYPE_CHOICES = [
        ("normal", "Normal"),
        ("refund", "Refund"),
        ("paylater", "Pay Later"),
    ]

    txnid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    txn_date = models.DateField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="categories")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, related_name="sub_categories")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, related_name="payment_method")

    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPE_CHOICES, default="normal")

    refund = models.ForeignKey("Refund", on_delete=models.SET_NULL, null=True, blank=True, related_name="refund_transactions")
    paylater = models.ForeignKey("PayLater", on_delete=models.SET_NULL, null=True, blank=True, related_name="paylater_transactions")

    def __str__(self):
        return f"{self.type.title()} - {self.category.category_name if self.category else 'No Category'}"


class Refund(models.Model):
    REFUND_MODE_CHOICES = [
        ("full", "Full Refund"),
        ("partial", "Partial Refund"),
    ]

    refundid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="refund_transaction", null=True, blank=True)
    title = models.CharField(max_length=255)
    mode = models.CharField(max_length=10, choices=REFUND_MODE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_date = models.DateField()
    refunded = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund ({self.mode.title()}) - {self.amount} for {self.transaction.name if self.transaction else 'No Transaction'}"


class PayLater(models.Model):
    paylaterid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="paylater_transaction", null=True, blank=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PayLater {self.amount} due on {self.due_date} for {self.transaction.name if self.transaction else 'No Transaction'}"
