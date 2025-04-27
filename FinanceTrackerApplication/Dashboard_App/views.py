from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from datetime import datetime, timedelta
from django.utils import timezone
from userModule_App.views import getUserData
from Transactions_App.models import Transaction,Refund,PayLater

def userDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')

    # Get filter type from URL query parameters
    filter_type = request.GET.get('filter', 'this_month')  # Default to 'this_month' if not provided

    today = timezone.now().date()
    filter_dates = {
        'this_month': (today.replace(day=1), today),
        'last_15_days': (today - timedelta(days=15), today),
        'last_week': (today - timedelta(days=7), today),
        'last_45_days': (today - timedelta(days=45), today),
        'last_3_months': (today - timedelta(days=90), today),
        'last_6_months': (today - timedelta(days=180), today),
        'last_year': (today - timedelta(days=365), today),
    }

    # Get the date range for the selected filter
    start_date, end_date = filter_dates.get(filter_type, (today.replace(day=1), today))

    # Fetch the user-specific data
    userid = request.session.get("user_id")
    user = getUserData(userid)

    # Filter transactions based on the selected date range
    transactions = Transaction.objects.filter(
        user=user, 
        txn_date__range=(start_date, end_date),
        status=True  # Ensure transaction is active/valid
    ).select_related('category', 'subcategory', 'payment_method')

    # Fetch related data for other categories (refunds, paylater)
    refunds = Refund.objects.filter(
        transaction__user=user, 
        transaction__txn_date__range=(start_date, end_date),
        refunded=False  # Pending refunds
    )

    paylaters = PayLater.objects.filter(
        transaction__user=user, 
        transaction__txn_date__range=(start_date, end_date)
    )

    # Calculate amounts for income, expense, refunds, and paylater
    incomeAmt = sum(txn.amount for txn in transactions if txn.type == "income")
    expenseAmt = sum(txn.amount for txn in transactions if txn.type == "expense")
    refundAmt = sum(refund.amount for refund in refunds)
    paylaterAmt = sum(paylater.amount for paylater in paylaters)

    # Context to pass to the template
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'filter_type': filter_type,
        'incomeAmt': incomeAmt,
        'expenseAmt': expenseAmt,
        'refundAmt': refundAmt,
        'paylaterAmt': paylaterAmt,
        'transactions': transactions,
        'refunds': refunds,
        'paylaters': paylaters,
    }

    return render(request, 'userDashboard.html', context)

def defaultRedirection(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    return redirect('userDashboard')