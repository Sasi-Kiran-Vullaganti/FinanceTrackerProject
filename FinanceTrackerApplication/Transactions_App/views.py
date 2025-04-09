from django.shortcuts import render,redirect,get_object_or_404
from userModule_App.userValidations import checkLoginStatus 
from userModule_App.models import UserProfile
from userModule_App.views import getUserData
from .models import Category,Subcategory,Transaction,PaymentMethod,Refund,PayLater
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def transactionDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')
    userid = request.session.get("user_id")
    user = getUserData(userid)
    transactions = (
        Transaction.objects.filter(user=user,status=True)
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

        # Initialize error list
        errors = []

        # Validate required fields and their constraints
        if not transaction_name or not (3 <= len(transaction_name) <= 12):
            errors.append("Transaction name is required and must be between 3 and 12 characters.")
        if not transaction_type:
            errors.append("Transaction type is required.")
        if not transaction_amount or not transaction_amount.isdigit() or int(transaction_amount) <= 0:
            errors.append("Transaction amount is required and must be a positive number.")
        if not transaction_date:
            errors.append("Transaction date is required.")
        else:
            try:
                transaction_date_obj = datetime.strptime(transaction_date, '%Y-%m-%d')
                if transaction_date_obj > datetime.now():
                    errors.append("Transaction date cannot be in the future.")
            except ValueError:
                errors.append("Transaction date must be in the format YYYY-MM-DD.")
        
        if not transaction_category:
            errors.append("Transaction category is required.")
        if not transaction_subcategory:
            errors.append("Transaction subcategory is required.")
        if transaction_notes and len(transaction_notes) > 255:
            errors.append("Transaction notes cannot exceed 255 characters.")

        # Validate refund fields if advanced_transaction_type is 'refund'
        if advanced_transaction_type == 'refund' and transaction_type == 'expense':
            if not refund_title or not (3 <= len(refund_title) <= 15):
                errors.append("Refund title is required and must be between 3 and 12 characters.")
            if not refund_mode:
                errors.append("Refund mode is required.")
            if not refund_amount or not refund_amount.isdigit() or int(refund_amount) <= 0:
                errors.append("Refund amount is required and must be a positive number.")
            if not refund_date:
                errors.append("Refund date is required.")
            else:
                try:
                    refund_date_obj = datetime.strptime(refund_date, '%Y-%m-%d')
                    if refund_date_obj < datetime.now():
                        errors.append("Refund date cannot be in the past.")
                except ValueError:
                    errors.append("Refund date must be in the format YYYY-MM-DD.")

        # Validate paylater fields if advanced_transaction_type is 'paylater'
        if advanced_transaction_type == 'paylater' and transaction_type == 'expense':
            if not paylater_title or not (3 <= len(paylater_title) <= 20):
                errors.append("Paylater title is required and must be between 3 and 12 characters.")
            if not paylater_amount or not paylater_amount.isdigit() or int(paylater_amount) <= 0:
                errors.append("Paylater amount is required and must be a positive number.")
            if not due_date:
                errors.append("Due date is required.")
            else:
                try:
                    due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
                    if due_date_obj < datetime.now():
                        errors.append("Due date must be in the future.")
                except ValueError:
                    errors.append("Due date must be in the format YYYY-MM-DD.")

        # If there are validation errors, return to the form with errors
        if errors:
            print(errors)
            return render(request, 'addTransaction.html', {'user': user, 'errors': errors})

        # ForeignKeys
        try:
            category_instance = Category.objects.get(category_id=transaction_category)
            subcategory_instance = Subcategory.objects.get(subcategory_id=transaction_subcategory)
            paymentMethodID = PaymentMethod.objects.get(payment_method_id=payment_method) if payment_method else None
        except ObjectDoesNotExist as e:
            errors.append(f"Error fetching related data: {str(e)}")
            return render(request, 'addTransaction.html', {'user': user, 'errors': errors})

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

        statusVal = True
        if advanced_transaction_type == 'paylater':
            statusVal = False

        # Create Transaction
        transaction_instance = Transaction.objects.create(
            name=transaction_name,
            amount=transaction_amount,
            type=transaction_type,
            txn_date=transaction_date,
            user=user,
            category=category_instance,
            subcategory=subcategory_instance,
            payment_method=paymentMethodID,  # can be None
            notes=transaction_notes,
            expense_type=advanced_transaction_type or 'normal',
            refund=refund_instance,
            paylater=paylater_instance,
            status = statusVal
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

def TransactionDetails(request, txn_id):
    transaction = get_object_or_404(Transaction, txnid=txn_id)

    # Check if Refund or PayLater exists for this transaction
    refund_details = Refund.objects.filter(transaction=transaction).first()
    paylater_details = PayLater.objects.filter(transaction=transaction).first()

    context = {
        'transaction': transaction,
        'refund_details': refund_details,
        'paylater_details': paylater_details,
    }
    return render(request,'TransactionDetails.html',context)