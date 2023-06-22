from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
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



# Function Based View


# 1) EndPoint All_Products search by name
@api_view(["GET"])
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
    print(serializer.data[1]["id"])
    return Response(data)


# 2) Get User info and Update
@api_view(["GET", "PUT"])
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

# 5) Checkout with sending email and emptying cart related to this user
@api_view(['GET'])
def Checkout_pk(request, pk):
    # Retrieve the user and their cart
    user = get_object_or_404(User, id=pk)
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return Response({'detail': 'Cart is empty'}, status=status.HTTP_404_NOT_FOUND)

    
    send_mail(
        'Your order has been processed',
        'Thank you for your purchase!',
        'hatemgad98@gmail.com',
        [user.user_email],
        fail_silently=False,
    )

    # Empty the user's cart
    cart.product.clear()

    return Response({'detail': 'Checkout successful'}, status=status.HTTP_200_OK)


# 10) wish-list endpoint that get all products user liked
@api_view(["GET"])
def Wishlist_pk(request, pk):
    try:
        wishlistUser = get_object_or_404(User, id=pk)
        wishlist = get_object_or_404(WishList, user=wishlistUser)

    except WishList.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    products = wishlist.product.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)