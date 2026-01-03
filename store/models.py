from django.db import models
from django.contrib.auth.models import User

# Product model
class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.CharField(
        max_length=5000,
        default="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAADACAMAAAB/Pny7AAAAilBMVEX..."
    )
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name

# User Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"

# Items inside a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.price * self.quantity

# Order model
class Order(models.Model):
    STATUS_CHOICE =[
        ('PENDING','Pending'),
        ('PAID','Paid'),
        ('SHIPPED','Shipped'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled'),

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)


    def __str__(self):
        return f"Order #{self.id} - {self.status}"

# Items inside an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def sub_total(self):
        return self.price * self.quantity
