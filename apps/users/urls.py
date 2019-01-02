from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login_for_modal/', views.LoginModalView.as_view(), name='login_for_modal'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forgot_pwd/', views.ForgetPwdView.as_view(), name='forgot_pwd'),
    path('', views.UserInfoView.as_view(), name='user_info'),
    path('icon/', views.UserIcon.as_view(), name='user_icon'),
    path('icon/change/', views.ChangeIcon.as_view(), name='change_icon'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    ]
