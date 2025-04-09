from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.views import getUserData
from Transactions_App.models import PayLater
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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

def getPayLaterDetails(request):
    paylaterid = request.GET.get('paylaterid')
    paylater = get_object_or_404(PayLater, paylaterid=paylaterid)
    data = {
        'title': paylater.title,
        'amount': str(paylater.amount),
        'due_date': paylater.due_date.strftime("%d-%m-%Y"),
    }
    return JsonResponse(data)

@csrf_exempt
def payLaterPayment(request):
    if request.method == "POST":
        paylaterid = request.POST.get('paylaterid')
        paylater = get_object_or_404(PayLater, paylaterid=paylaterid)
        transaction = paylater.transaction
        
        paylater.paid = True
        paylater.save()

        transaction.status = True
        transaction.save()

        return JsonResponse({'status': 'success'})
