from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 

# Create your views here.
def userDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return render(request,'userDashboard.html')

def defaultRedirection(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return redirect('userDashboard')