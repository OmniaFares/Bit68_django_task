from app.models import Cart, Order, Product
from rest_framework.views import APIView
from .serializer import UserSerializer, ProductSerializer, OrderSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


class ProductView(APIView):
    serializer_class = ProductSerializer

    def post(self, request):
        product = self.serializer_class(data=request.data)
        if Product.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        products = Product.objects.all().order_by('price')
        products = self.serializer_class(products, many=True)
        return Response(products.data)


class CartView(APIView):
    serializer_class = CartSerializer


class OrderView(APIView):
    serializer_class = OrderSerializer


