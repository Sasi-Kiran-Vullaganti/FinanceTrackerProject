from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.models import UserProfile
from userModule_App.views import getUserData

# Create your views here.
def transactionDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return render(request,'userTransactionDashboard.html')

def addTransaction(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    return render(request,'addTransaction.html',{'user':user})