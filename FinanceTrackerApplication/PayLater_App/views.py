from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.views import getUserData
from Transactions_App.models import PayLater

# Create your views here.
def payLaterDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    paylaters = (
        PayLater.objects.filter(transaction__user=user)
        .select_related('transaction')
    )
    context = {
        'paylaters': paylaters,
    }
    return render(request,'PayLaterDashboard.html',context)