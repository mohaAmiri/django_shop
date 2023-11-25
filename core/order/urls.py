from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('<int:id>/', views.order_detail, name='order-detail'),
    path('create/', views.order_create, name='order-create'),
]
