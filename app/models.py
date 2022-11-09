from django.db import models
import user.models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Cart(models.Model):
    user = models.OneToOneField('user.CustomUser', related_name="user_cart", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="products_carts")


class Order(models.Model):
    user = models.ForeignKey('user.CustomUser', related_name="order_user", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="order_cart", on_delete=models.CASCADE)


