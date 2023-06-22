from django.db import models

# Create your models here.
class Products(models.Model):
    product_name=models.CharField(max_length=50)
    product_description=models.TextField(max_length=255)
    product_quantity=models.PositiveIntegerField()
    product_image=models.ImageField()
    def __str__(self):
        return self.product_name


class User(models.Model):
    user_fname=models.CharField(max_length=50)
    user_lname=models.CharField(max_length=50)
    user_email=models.CharField(max_length=100,unique=True)
    user_password=models.CharField(max_length=150)
    user_image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.user_email
    
class Cart(models.Model):
    total_price=models.DecimalField(decimal_places=2,max_digits=10)
    product=models.ManyToManyField(Products, related_name='cart')
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self
    
    
class WishList(models.Model):
    product=models.ManyToManyField(Products)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self
    
    

