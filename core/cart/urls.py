from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('add/<int:id>/', views.add_cart, name='add-cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove-cart'),
    path('add_single/<int:id>/', views.add_single, name='add-single'),
    path('remove_single/<int:id>/', views.remove_single, name='remove-single'),
    path('compare/<int:id>/', views.compare, name='compare'),
    path('removecompare/<int:id>/', views.remove_compare, name='remove-compare'),
    path('showcompare/', views.show_compare, name='show-compare'),
]
