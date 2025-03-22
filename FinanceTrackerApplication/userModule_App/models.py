import random
import string
from django.db import models
from django.utils.timezone import now

def generate_userid():
    """Generate a User ID in the format USR+7 random digits (e.g., USR1234567)."""
    return f"USR{''.join(random.choices(string.digits, k=7))}"

class UserProfile(models.Model):
    userid = models.CharField(max_length=10, primary_key=True, default=generate_userid, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255) 
    
    GENDER_CHOICES = [
        ('M', 'M'),
        ('F', 'F'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.userid})"
