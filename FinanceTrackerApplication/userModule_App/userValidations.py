import re
from .models import UserProfile
from django.shortcuts import redirect

def checkLoginStatus(request):
    if not request.session.get("is_authenticated"):
        print('login required')
        return True

def user_registration_validation(data):
    errors = []

    # Name validation (3 to 15 characters, only letters and spaces)
    if not data.get("name") or not re.match(r"^[A-Za-z\s]{3,15}$", data["name"]):
        errors.append("Name must be between 3 and 15 characters and contain only letters.")

    # Email validation (basic format check)
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data.get("email", "")):
        errors.append("Enter a valid email address.")

    # Check if email is unique
    if UserProfile.objects.filter(email=data.get("email")).exists():
        errors.append("Email already exists. Please use another email.")

    # Phone validation (exactly 10 digits)
    if not data.get("phone") or not re.match(r"^\d{10}$", data["phone"]):
        errors.append("Phone number must be exactly 10 digits.")

    # Check if phone number is unique
    if UserProfile.objects.filter(phone=data.get("phone")).exists():
        errors.append("Phone number already registered.")

    # Password validation (one uppercase, one lowercase, one digit, one symbol, min 6 chars)
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
    if not re.match(password_regex, data.get("password", "")):
        errors.append("Password must be at least 6 characters long and include one uppercase letter, one lowercase letter, one number, and one special character.")

    # Gender validation
    if data.get("gender") not in ["M", "F"]:
        errors.append("Invalid gender selected.")

    # Currency validation
    if data.get("currency") not in ["USD", "INR"]:
        errors.append("Invalid currency selected.")

    return errors
