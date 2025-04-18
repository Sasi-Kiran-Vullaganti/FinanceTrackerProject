from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.models import UserProfile
from Transactions_App.models import Category,Subcategory,PaymentMethod

# Create your views here.
def reportsDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    # Get current user's profile
    user_profile = UserProfile.objects.get(userid=request.session.get("user_id"))

    # Fetch all categories for the user
    categories = Category.objects.filter(user=user_profile).prefetch_related('subcategories')

    # Fetch all subcategories related to user's categories
    subcategories = Subcategory.objects.filter(category__user=user_profile)

    # Fetch all payment methods for the user
    payment_methods = PaymentMethod.objects.filter(user=user_profile)

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'payment_methods': payment_methods,
    }

    return render(request, 'ReportsDashboard.html', context)
    return render(request,'ReportsDashboard.html')