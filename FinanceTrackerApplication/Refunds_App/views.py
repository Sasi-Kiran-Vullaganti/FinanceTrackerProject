from django.shortcuts import render,redirect,get_object_or_404
from userModule_App.userValidations import checkLoginStatus 
from Transactions_App.models import Refund
from userModule_App.views import getUserData
from django.views.decorators.http import require_POST
from Transactions_App.models import Transaction,Refund,PayLater,Category,Subcategory,PaymentMethod
from django.utils.timezone import now

# Create your views here.
def refundsDashboard(request):
    logincheck = checkLoginStatus(request)
    if logincheck:
        return redirect('userLogin')

    userid = request.session.get("user_id")
    user = getUserData(userid)

    filter_type = request.GET.get('filter', 'all')

    # Define filter conditions for refunds
    filter_conditions = {
        'pendingrefunds': {'refunded': False},
        'refunded': {'refunded': True},
    }

    refunds = Refund.objects.filter(transaction__user=user).select_related('transaction')

    if filter_type in filter_conditions:
        refunds = refunds.filter(**filter_conditions[filter_type])

    context = {
        'refunds': refunds,
        'filter_type': filter_type,  # useful for showing active filter in template
    }
    return render(request, 'RefundsDashboard.html', context)


@require_POST
def mark_refund_received(request):
    refundid = request.POST.get("refundid")
    refund = get_object_or_404(Refund, refundid=refundid)

    if not refund.refunded:
        # Mark refund as received
        refund.refunded = True
        refund.save()

        # Create a new income transaction
        original_txn = refund.transaction
        income_txn = Transaction.objects.create(
            name=f"Refund: {refund.title}",
            amount=refund.amount,
            type="refunded",
            notes=f"Refund received for transaction: {original_txn.name if original_txn else 'Unknown'}",
            txn_date=now().date(),
            status=True,  # Optional: mark as successful
            user=original_txn.user if original_txn else request.user.profile,  # fallback to request user
            category=original_txn.category if original_txn else None,
            subcategory=original_txn.subcategory if original_txn else None,
            payment_method=original_txn.payment_method if original_txn else None,
            expense_type="refund",  # Refund received is not an expense
            refund=refund  # Link back to Refund
        )

    return redirect("refundsDashboard")