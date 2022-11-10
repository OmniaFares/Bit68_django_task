from django.urls import path, include
from .views import ProductView, OrderView, CartView

urlpatterns = [
    path('product', ProductView.as_view()),
    path('order', OrderView.as_view()),
    path('cart', CartView.as_view()),
]