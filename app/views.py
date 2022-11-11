from app.models import Cart, Order, Product
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializer import UserSerializer, ProductSerializer, OrderSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


@api_view(['GET'])
def get_user_cart(request, id):
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            user_cart = Cart.objects.get(id=serializer.data['cart'])
            return Response(CartSerializer(user_cart).data)


@api_view(['GET'])
def get_user_orders(request, id):
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            try:
                user_orders = Order.objects.get(id=serializer.data['orders'])
            except Order.DoesNotExist:
                return Response({"Not Found": "This User hasn't create any orders yet"})

            return Response(OrderSerializer(user_orders).data)


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
        if request.data:
            product = Product.objects.get(name=request.data['name'])
            product = self.serializer_class(product)
            return Response(product.data)
        else:
            products = Product.objects.all().order_by('price')
            products = self.serializer_class(products, many=True)
            return Response(products.data)


class CartView(APIView):
    serializer_class = CartSerializer

    def post(self, request):
        try:
            user = CustomUser.objects.get(id=request.data['user'])
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            products = Product.objects.get(id=request.data['products'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(user=user)
        cart.products.add(products)

        return Response({"success": "Product added successfully to cart", "Cart": CartSerializer(cart).data})


class OrderView(APIView):
    serializer_class = OrderSerializer

    def post(self, request):
        try:
            user = CustomUser.objects.get(id=request.data['user'])
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(id=request.data['cart'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(user=user, cart=cart)

        return Response({"success": "Order has created successfully", "Order": OrderSerializer(order).data})


