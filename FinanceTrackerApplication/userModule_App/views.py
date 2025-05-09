import random
import re
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password ,check_password
from .models import UserProfile
from django.contrib.auth import authenticate, login
from .userValidations import user_registration_validation 
from userModule_App.userValidations import checkLoginStatus 
from Transactions_App.models import Category,Subcategory,PaymentMethod,Transaction,Refund,PayLater
from django.db.models import Sum

def getUserData(userid):
    user = UserProfile.objects.get(userid=userid)
    return user

def generate_unique_userid():
    while True:
        userid = f"USR{''.join(random.choices(string.digits, k=7))}"
        if not UserProfile.objects.filter(userid=userid).exists():
            return userid

def UserProfileView(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    
    userid = request.session.get("user_id")
    user = getUserData(userid)
    
    # Get overall totals grouped by category and subcategory
    category_data = []
    categories = Category.objects.filter(user=user)
    
    for category in categories:
        # Calculate total for income and expense by category
        category_income_total = Transaction.objects.filter(user=user, category=category, type='income').aggregate(total=Sum('amount'))['total'] or 0
        category_expense_total = Transaction.objects.filter(user=user, category=category, type='expense').aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate the total of income and expense for this category
        category_total = category_income_total + category_expense_total
        
        subcategory_data = []
        
        # Calculate income and expense totals for each subcategory
        subcategories = Subcategory.objects.filter(category=category)
        for subcat in subcategories:
            sub_income_total = Transaction.objects.filter(user=user, subcategory=subcat, type='income').aggregate(total=Sum('amount'))['total'] or 0
            sub_expense_total = Transaction.objects.filter(user=user, subcategory=subcat, type='expense').aggregate(total=Sum('amount'))['total'] or 0
            
            subcategory_data.append({
                'name': subcat.subcategory_name,
                'income_total': sub_income_total,
                'expense_total': sub_expense_total,
            })
        
        category_data.append({
            'name': category.category_name,
            'income_total': category_income_total,
            'expense_total': category_expense_total,
            'category_total': category_total,  # Added the sum here
            'subcategories': subcategory_data
        })

    # Payment method totals
    payment_data = []
    payment_methods = PaymentMethod.objects.filter(user=user)
    for pm in payment_methods:
        pm_total = Transaction.objects.filter(user=user, payment_method=pm).aggregate(total=Sum('amount'))['total'] or 0
        payment_data.append({
            'name': pm.payment_method_name,
            'type': pm.payment_type,
            'total': pm_total
        })

    context = {
        "userData": user,
        "category_data": category_data,
        "payment_data": payment_data
    }
    return render(request, 'UserProfile.html', context)


def ChangePassword(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        userid = request.session.get("user_id")
        try:
            user = UserProfile.objects.get(userid=userid)
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("ChangePassword")
        
        # Validate old password
        if not check_password(old_password, user.password):
            messages.error(request, "Old password is incorrect.")
            return redirect("ChangePassword")
        
        # Check if new password matches confirm
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return redirect("ChangePassword")
        
        # Regex validation
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        if not re.match(password_regex, new_password):
            messages.error(request, "Password must be at least 6 characters long and include one uppercase letter, one lowercase letter, one number, and one special character.")
            return redirect("ChangePassword")

        # Save new password
        user.password = make_password(new_password)
        user.last_updated = now()
        user.save()

        messages.success(request, "Password changed successfully.")
        return redirect("userDashboard")

    return render(request,'ChangePassword.html')

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

                user.last_login = now()
                user.save(update_fields=["last_login"])

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