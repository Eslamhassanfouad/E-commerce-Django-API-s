from rest_framework import serializers
from .models import User,Products,Cart,WishList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
        
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
        
        
class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model=WishList
        fields='__all__'