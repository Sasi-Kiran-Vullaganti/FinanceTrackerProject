from django.shortcuts import render,redirect
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.models import UserProfile
from userModule_App.views import getUserData
from .models import Category,Subcategory,Transaction,PaymentMethod,Refund,PayLater
from django.contrib import messages

# Create your views here.
def transactionDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    transactions = (
        Transaction.objects.filter(user=user)
        .select_related(
            'category', 
            'subcategory', 
            'payment_method', 
            'refund', 
            'paylater'
        )
        .order_by('-txn_date', '-added_on')  # Latest first
    )
    incomeAmt = 0
    expenseAmt = 0
    refundAmt = 0
    paylaterAmt = 0
    for i in transactions:
        if i.type == "income":
            incomeAmt = incomeAmt + int(i.amount)
        else:
            if i.expense_type == 'normal':
                expenseAmt = expenseAmt + int(i.amount)
            elif i.expense_type == 'refund':
                refundAmt = refundAmt + int(i.amount)
            elif i.expense_type == 'paylater':
                paylaterAmt = paylaterAmt + int(i.amount)



    refunds = (
        Refund.objects.filter(transaction__user=user)
        .select_related('transaction')
    )

    paylaters = (
        PayLater.objects.filter(transaction__user=user)
        .select_related('transaction')
    )

    balance_amt = incomeAmt - expenseAmt - refundAmt - paylaterAmt

    context = {
        'transactions': transactions,
        'refunds': refunds,
        'paylaters': paylaters,
        'incomeAmt' : incomeAmt,
        'expenseAmt' : expenseAmt,
        'refundAmt' : refundAmt,
        'paylaterAmt' : paylaterAmt,
        'balanceAmt' : balance_amt
    }
    return render(request,'userTransactionDashboard.html',context)

def addTransaction(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    if request.method == "POST":
        # Get form data
        transaction_name = request.POST.get('transaction_name')
        transaction_type = request.POST.get('transaction_type')
        transaction_amount = request.POST.get('transaction_amount')
        transaction_date = request.POST.get('transaction_date')
        transaction_category = request.POST.get('transaction_category')
        transaction_subcategory = request.POST.get('transaction_subcategory')
        payment_method = request.POST.get('payment_method')  # may be None
        transaction_notes = request.POST.get('transaction_notes')
        advanced_transaction_type = request.POST.get('advanced_transaction_type')
        refund_title = request.POST.get('refund_title')
        refund_mode = request.POST.get('refund_mode')
        refund_amount = request.POST.get('refund_amount')
        refund_date = request.POST.get('refund_date')
        paylater_title = request.POST.get('paylater_title')
        paylater_amount = request.POST.get('paylater_amount')
        due_date = request.POST.get('due_date')

        # ForeignKeys
        CategoryID = Category.objects.get(category_id=transaction_category)
        SubcategoryID = Subcategory.objects.get(subcategory_id=transaction_subcategory)

        paymentMethodID = None  # Default None
        if payment_method:  # Only fetch if provided
            paymentMethodID = PaymentMethod.objects.get(payment_method_id=payment_method)

        refund_instance = None
        paylater_instance = None

        # Create Refund instance if required
        if advanced_transaction_type == 'refund' and transaction_type == 'expense':
            refund_instance = Refund.objects.create(
                title=refund_title,
                mode=refund_mode,
                amount=refund_amount,
                refund_date=refund_date
            )

        # Create PayLater instance if required
        if advanced_transaction_type == 'paylater' and transaction_type == 'expense':
            paylater_instance = PayLater.objects.create(
                title=paylater_title,
                amount=paylater_amount,
                due_date=due_date
            )

        # Create Transaction
        transaction_instance = Transaction.objects.create(
            name=transaction_name,
            amount=transaction_amount,
            type=transaction_type,
            txn_date=transaction_date,
            user=user,
            category=CategoryID,
            subcategory=SubcategoryID,
            payment_method=paymentMethodID,  # can be None
            notes=transaction_notes,
            expense_type=advanced_transaction_type or 'normal',
            refund=refund_instance,
            paylater=paylater_instance,
        )

        # Update Refund / PayLater with transaction link
        if refund_instance:
            refund_instance.transaction = transaction_instance
            refund_instance.save()

        if paylater_instance:
            paylater_instance.transaction = transaction_instance
            paylater_instance.save()

        return redirect("transactionDashboard")



    return render(request,'addTransaction.html',{'user':user})