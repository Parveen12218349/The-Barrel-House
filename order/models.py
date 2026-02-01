# orders/models.py

from django.db import models
from products.models import Product
from users.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # ✅ Add defaults or make nullable to prevent migration errors
    shipping_address = models.TextField(default="Not Provided")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username if self.buyer else 'Unknown'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at purchase time

    def __str__(self):
        return f"{self.quantity} × {self.product.name} in Order #{self.order.id}"
