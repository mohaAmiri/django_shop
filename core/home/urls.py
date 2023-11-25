from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.all_products, name='products'),
    path('detail/<int:id>/', views.product_detail, name='product-detail'),
    path('category/<slug>/<int:id>/', views.all_products, name='category'),
    path('like/<int:id>/', views.product_like, name='like'),
    path('unlike/<int:id>/', views.product_unlike, name='unlike'),
    path('comment/<int:id>/', views.product_comment, name='comment'),
    path('reply/<int:id>/<int:comment_id>/', views.reply_comment, name='reply-comment'),
    path('comlike/<int:id>/', views.comment_like, name='comment-like'),
]
