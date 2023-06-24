from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Products(models.Model):
    product_name=models.CharField(max_length=50)
    product_description=models.TextField(max_length=255)
    product_quantity=models.PositiveIntegerField()
    product_image=models.ImageField()
    def __str__(self):
        return self.product_name


class User(AbstractUser):
    email=models.EmailField(max_length=255,unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.email
    
class Cart(models.Model):
    total_price=models.DecimalField(decimal_places=2,max_digits=10)
    product=models.ManyToManyField(Products, related_name='cart')
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return 'Cart'
    
    
class WishList(models.Model):
    product=models.ManyToManyField(Products)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return 'wish'
    
    

