from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.refundsDashboard,name='refundsDashboard'),
    path('mark-received', views.mark_refund_received, name='mark_refund_received'),

]
