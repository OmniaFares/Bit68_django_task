from django.urls import path, include
from .views import ProductView, OrderView, CartView
from app import views

urlpatterns = [
    path('product', ProductView.as_view()),
    path('order', OrderView.as_view()),
    path('cart', CartView.as_view()),
    path('get_user_cart/<int:id>', views.get_user_cart),
    path('get_user_orders/<int:id>', views.get_user_orders),
]