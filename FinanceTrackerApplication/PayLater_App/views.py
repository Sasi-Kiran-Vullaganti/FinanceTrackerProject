from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 

# Create your views here.
def payLaterDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return render(request,'PayLaterDashboard.html')