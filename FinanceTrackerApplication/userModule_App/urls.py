from django.urls import path
from . import views

urlpatterns = [
    path('login',views.userLogin,name='userLogin'),
    path('register',views.userRegister,name='userRegister'),
    path('logout',views.userLogout,name='userLogout'),
    path('ChangePassword',views.ChangePassword,name='ChangePassword'),
    path('UserProfile/me',views.UserProfileView,name='UserProfileUrl')
]
