from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('profile/', views.profile_view, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),


]
