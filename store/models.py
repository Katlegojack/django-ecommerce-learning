from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.CharField(max_length=5000, default="data:image/png;base64,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")
    created_at = models.DateTimeField(auto_now_add=True)
    #slug = models.SlugField(unique=True,blank =True)
   
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey('Products',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    total_price =models.DecimalField(max_digits=15,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Oder #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    quantity = models.PositiveIntegerField()



                