from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 

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
    return render(request,'addTransaction.html')