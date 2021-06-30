from django.urls import path,include

from .views import (
    login_fn,
    register,
    home,
    logout_fn,
    account_detail,
    change_password,
    CounterBaseOTPView,
)

app_name = "account"
urlpatterns = [
    path('login',login_fn,name="login"),
    path('register',register,name="register",),
    path('home/',home,name="home"),
    path('logout/',logout_fn,name="logout"),
    path('account_detail',account_detail,name="account-detail"),
    path('change_pswd/',change_password,name="change-password"),
    #get_otp
    path("verify/<phone>/",CounterBaseOTPView.as_view(),name="otp")
]
