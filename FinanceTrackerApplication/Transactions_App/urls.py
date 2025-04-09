from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.transactionDashboard,name='transactionDashboard'),
    path('addTransaction',views.addTransaction,name='addTransaction'),
    path('Transaction-Details/<uuid:txn_id>/',views.TransactionDetails,name='TransactionDetails'),
]
