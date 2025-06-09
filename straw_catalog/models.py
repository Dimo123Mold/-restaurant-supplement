from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Avg
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to='dishes/', blank=True, null=True)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=0)
    @property
    def average_rating(self):
        avg = self.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg is not None else 0
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.dish.price * self.quantity

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Готівка при отриманні'),
        ('online', 'Онлайн-оплата'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='current_orders')
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE,  related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price
