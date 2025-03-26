from django.shortcuts import render

# Create your views here.
def transactionDashboard(request):
    return render(request,'userTransactionDashboard.html')

def addTransaction(request):
    return render(request,'addTransaction.html')