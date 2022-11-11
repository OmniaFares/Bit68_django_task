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
        # check if user exists
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # return user cart with its details
        if request.method == 'GET':
            serializer = UserSerializer(user)
            user_cart = Cart.objects.get(id=CartSerializer(user.cart).data['id'])
            return Response(CartSerializer(user_cart).data)


@api_view(['GET'])
def get_user_orders(request, id):
        # check if user exists
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # return details of user orders
        if request.method == 'GET':
            try:
                output = []
                orders = OrderSerializer(user.orders.all(), many=True).data
                for i in range(len(orders)):
                    serialized_order = OrderSerializer(orders[i]).data
                    output.append(OrderSerializer(Order.objects.get(id=serialized_order['id'])).data)
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(output)


class ProductView(APIView):
    serializer_class = ProductSerializer

    def post(self, request):
        product = self.serializer_class(data=request.data)

        # check if product is duplicate
        if Product.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')

        # add new product
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        # get specific product by name
        if request.data:
            product = Product.objects.get(name=request.data['name'])
            product = self.serializer_class(product)
            return Response(product.data)
        # get all products ordered by price
        else:
            products = Product.objects.all().order_by('price')
            products = self.serializer_class(products, many=True)
            return Response(products.data)


class CartView(APIView):
    serializer_class = CartSerializer

    # user add product to cart
    def post(self, request):
        # check if user exists
        try:
            user = CustomUser.objects.get(id=request.data['user'])
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check if product exists
        try:
            products = Product.objects.get(id=request.data['products'])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart.objects.get(user=user)
        cart.products.add(products)

        return Response({"success": "Product added successfully to cart", "Cart": CartSerializer(cart).data})


class OrderView(APIView):
    serializer_class = OrderSerializer

    # user make new order
    def post(self, request):
        # check if user exists
        try:
            user = CustomUser.objects.get(id=request.data['user'])
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check if cart exists
        try:
            cart = Cart.objects.get(id=request.data['cart'])
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(user=user, cart=cart)
        user.orders.add(order)

        return Response({"success": "Order has created successfully", "Order": OrderSerializer(order).data})


