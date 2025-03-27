from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 

# Create your views here.
def refundsDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return render(request,'RefundsDashboard.html')