from django.urls import path
from . import views

app_name = 'accounting'
urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('changepass/', views.change_password, name='change-password'),
    path('login_phone/', views.phone, name='phone_login'),
    path('verify/', views.verify, name='verify'),
    path('active/<uidb64>/<token>/', views.RegisterEmail.as_view(), name='active-account'),
    path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/done/', views.DonePassword.as_view(), name='reset-done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password-reset-confirm'),
    path('confirm/done/', views.Complete.as_view(), name='complete'),
]
