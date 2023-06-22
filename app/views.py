from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view  
from .models import User,Cart,Products,WishList
from .serializers import ProductsSerializer,UserSerializer,CartSerializer,WishListSerializer
from rest_framework import status,filters
from rest_framework.response import Response

# Create your views here.



#i will be working with Function Based View

#1) EndPoint All_Products search by name
@api_view(['GET'])
def all_products(request,name):  
    
    product=Products.objects.filter(
        product_name=name
    )
    
    serializer=ProductsSerializer(product,many=True)
    data = [{'product_image': item['product_image'], 'product_name': item['product_name'] , 'product_quantity' : item['product_quantity']} for item in serializer.data]
    print(serializer.data[1]['id' ])
    return Response(data)


#2) Get User info and Update 
@api_view(['GET','PUT'])
def user_info(request,pk):
    user=get_object_or_404(User,pk=pk)
    if request.method=='GET':
        serializer=UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method=='PUT':
        serializer=UserSerializer(user=request.data)
        if serializer.is_valid():
            serializer.update(user,serializer.data)
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

