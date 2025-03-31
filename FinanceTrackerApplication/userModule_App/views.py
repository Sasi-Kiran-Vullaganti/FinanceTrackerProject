import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password ,check_password
from .models import UserProfile
from django.contrib.auth import authenticate, login
from .userValidations import user_registration_validation 
from userModule_App.userValidations import checkLoginStatus 

def getUserData(userid):
    user = UserProfile.objects.get(userid=userid)
    return user

def generate_unique_userid():
    while True:
        userid = f"USR{''.join(random.choices(string.digits, k=7))}"
        if not UserProfile.objects.filter(userid=userid).exists():
            return userid

# Create your views here.
def userLogin(request):
    logincheck = checkLoginStatus(request)
    if not logincheck:
        return redirect('userDashboard')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both fields are required.")
            return redirect("userLogin")

        try:
            user = UserProfile.objects.get(email=email)  
            if check_password(password, user.password):  
                request.session["is_authenticated"] = True
                request.session["user_id"] = user.userid  
                request.session["user_name"] = user.name  
                request.session["user_email"] = user.email  
                messages.success(request, "Login successful!")
                return redirect("userDashboard")  
            else:
                messages.error(request, "Invalid email or password.")
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid email or password.")
        return redirect("userLogin")
    return render(request,'userLogin.html')

def userRegister(request):
    logincheck = checkLoginStatus(request)
    if not logincheck:
        return redirect('userDashboard')
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "password": request.POST.get("password"),
            "gender": request.POST.get("gender"),
            "currency": request.POST.get("currency"),
        }
        errors = user_registration_validation(data)
        if UserProfile.objects.filter(email=data["email"]).exists():
            errors.append("Email is already registered.")
        if UserProfile.objects.filter(phone=data["phone"]).exists():
            errors.append("Phone number is already registered.")

        if errors:
            print(errors)
            return render(request, "userRegister.html", {"errors": errors, "data": data}) 
        user = UserProfile.objects.create(
            userid=generate_unique_userid(),
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            password=make_password(data["password"]),  
            gender=data["gender"],
            currency=data["currency"],
            date_created=now(),
            last_updated=now(),
        )
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("userLogin")  
    return render(request,'userRegister.html')

def userLogout(request):
    if request.session.get("is_authenticated"):
        request.session.flush()
        messages.success(request, "You have been logged out successfully.")
    return redirect("userLogin")