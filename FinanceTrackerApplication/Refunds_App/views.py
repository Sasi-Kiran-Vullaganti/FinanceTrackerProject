from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from Transactions_App.models import Refund
from userModule_App.views import getUserData

# Create your views here.
def refundsDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    refunds = (
        Refund.objects.filter(transaction__user=user)
        .select_related('transaction')
    )
    context = {
        'refunds': refunds,
    }
    return render(request,'RefundsDashboard.html',context)