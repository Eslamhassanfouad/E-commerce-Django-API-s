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
            send_mail(
            "Registration",
            "Thank you for registering in our application!",
            host_user,
            
            [request.data['email']],
            fail_silently=False,
            )
            serializer.save()

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

# Search For Products With Name
# @api_view(['GET'])
# def searchProduct(request, name):
#     matchedProducts = Products.objects.filter(product_name=name)
#     matchedProductsSerialized=ProductsSerializer(matchedProducts,many=True)
#     return Response(matchedProductsSerialized.data, status=200)

# @api_view(["GET"])
# def getAllProducts(request):
#     products = Products.objects.all()
#     serialized_Products = ProductsSerializer(products, many=True)
#     return Response(serialized_Products.data)


# # Get Specific Product
# @api_view(["GET"])
# def getProduct(request, id):
#     try:
#         product = Products.objects.get(id=id)
#         serialized_Product = ProductsSerializer(product)
#         return Response(serialized_Product.data, status=200)
#     except:
#         return Response({"Error - This Product Doesn’t Exist"}, status=400)


# # Add New Product
# @api_view(["GET", "POST"])
# def createProduct(request):
#     product = request.data
#     serialized_Product = ProductsSerializer(data=product)
#     if serialized_Product.is_valid():
#         serialized_Product.save()
#         return Response(serialized_Product.data, status=201)
#     else:
#         return Response(serialized_Product.errors, status=400)


# # Update Existing Product
# @api_view(["PUT"])
# def updateProduct(request, id):
#     try:
#         product = Products.objects.get(id=id)
#         for key, value in request.POST.items():
#             setattr(product, key, value)
#         serialized_Product = ProductsSerializer(product)
#         product.save()
#         return Response(serialized_Product.data, status=200)
#     except:
#         return Response({"Error - This Product Doesn’t Exist"}, status=400)


# Delete Existing Product
# @api_view(["DELETE"])
# def deleteProduct(request, id):
#     try:
#         product = Products.objects.get(id=id)
#         product.delete()
#         return Response("{} is deleted".format(product))
#         # return Response({`$productProduct Deleted`},status=200)
#     except:
#         return Response({"Error - This Product Does not Exist"}, status=400)


# Cart Functions
@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cart_List(request):
    # GET
    if request.method == 'GET':
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = CartSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)

#3.1 GET PUT DELETE (a sepcific user's cart)
@api_view(['GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cart_pk(request, pk):

    cartUser = get_object_or_404(User, id=pk)
    cart = get_object_or_404(Cart, user=cartUser)

    # GET
    if request.method == 'GET':
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data)
        
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


# 10) wish-list endpoint that get all products user liked


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
