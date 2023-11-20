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
]
