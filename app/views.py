from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .models import User, Cart, Products, WishList
from .serializers import (
    ProductsSerializer,
    UserSerializer,
    CartSerializer,
    WishListSerializer,
)
from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import authenticate, get_user_model


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from project import settings
from .models import User, Cart, Products, WishList
from .serializers import (
    ProductsSerializer,
    UserSerializer,
    CartSerializer,
    WishListSerializer,
)
from rest_framework import status, filters
from rest_framework.response import Response
from django.core.mail import send_mail
from config import host_user
# ------------------------Function Based Views-----------------------------


# User Functions


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # send_mail(
            # "Registration",
            # "Thank you for registering in our application!",
            # host_user,
            # [request.data['email']],
            # fail_silently=False,
            # )
            serializer.save()
            user = User.objects.filter(email=request.data['email']).first()
            Cart.objects.create(user=user, total_price=0)
            WishList.objects.create(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_info(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = UserSerializer(user=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.data)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Product Functions
# All Products search by name. (product image, name,and availability)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def all_products(request, name):
    product = Products.objects.filter(product_name=name)
    serializer = ProductsSerializer(product, many=True)
    data = [
        {
            "product_image": item["product_image"],
            "product_name": item["product_name"],
            "product_quantity": item["product_quantity"],
        }
        for item in serializer.data
    ]
    return Response(data)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getAllProducts(request):
    product = Products.objects.filter().all()
    serializer = ProductsSerializer(product, many=True)
    return Response(serializer.data)


# Get Product details search by name. (product name, image, number of items available, description)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def product_details(request, id):
    product = Products.objects.filter(product_id=id).first()
    serializer = ProductsSerializer(product)
    data = {
        "product_image": serializer.data["product_image"],
        "product_name": serializer.data["product_name"],
        "product_quantity": serializer.data["product_quantity"],
        "product_description": serializer.data["product_description"],
    }
    return Response(data)


class PostProduct(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

# Cart Functions

#3.1 GET PUT DELETE (a sepcific user's cart)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cart_pk(request, pk):
    try:
        cart = Cart.objects.filter(user_id=pk).first()
        if cart == None:
            raise Exception()
    except:
        return Response({"Details: Not Found"}, status= status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
        
    # PUT
    elif request.method == 'PUT':
        serializer = CartSerializer(cart, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        cart.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_cart_products(request, pk):
    try:
        user = User.objects.get(pk=pk)
        cart = Cart.objects.get(user=user)
        products = cart.products.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    except (User.DoesNotExist, Cart.DoesNotExist):
        raise Http404

@api_view(["POST"])
def AddToCart(request):
    # Get the product and user from the request data
    product_id = request.data.get('product_id')
    user_id = request.data.get('user_id')
    product = get_object_or_404(Products, id=product_id)
    user = get_object_or_404(User, id=user_id)

    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=user)

    # Add the product to the cart
    cart.product.add(product)
    total_price = sum(product.product_price for product in cart.product.all())
    cart.total_price = total_price
    cart.save()
    return Response({'message': 'Product added to cart', 'cart': cart.id, 'total_price': cart.total_price}, status=status.HTTP_200_OK)
    


# Checkout with sending email and emptying cart related to this user
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def Checkout_pk(request, pk):
    # Retrieve the user and their cart
    user = get_object_or_404(User, id=pk)
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return Response({"detail": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
    
    send_mail(
        "Your order has been processed",
        "Thank you for your purchase!",
        host_user,
        [user.email],
        fail_silently=False,
    )

    # Empty the user's cart
    cart.product.clear()
    return Response({"detail": "Checkout successful"}, status=status.HTTP_200_OK)


# Wishlist Functions

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def Wishlist_pk(request, pk):
    try:
        wishlistUser = get_object_or_404(User, id=pk)
        wishlist = get_object_or_404(WishList, user=wishlistUser)

    except WishList.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    products = wishlist.product.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def AddToWishlist(request):
    # Get the product and user from the request data
    product_id = request.data.get('product_id')
    user_id = request.data.get('user_id')
    product = get_object_or_404(Products, id=product_id)
    user = get_object_or_404(User, id=user_id)

    # Get or create the cart for the user
    wishlist, created = WishList.objects.get_or_create(user=user)

    # Add the product to the cart
    wishlist.product.add(product)
    total_price = sum(product.product_price for product in wishlist.product.all())
    wishlist.total_price = total_price
    wishlist.save()
    return Response({'message': 'Product added to wishlist',
                      'wishlist': wishlist.id}, 
                    status=status.HTTP_200_OK)
