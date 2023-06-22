from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view  
from .models import User,Cart,Products,WishList
from .serializers import ProductsSerializer,UserSerializer,CartSerializer,WishListSerializer
from rest_framework import status,filters
from rest_framework.response import Response

# Create your views here.

#i will be working with Function Based View


#1) This Is MO3 Speaking From The Other Side Of The World.

#Get All Products
@api_view(['GET'])
def getAllProducts(request):
    products = Products.objects.all()
    serialized_Products = ProductsSerializer(products, many=True)
    return Response(serialized_Products.data)

#Get Specific Product
@api_view(['GET'])
def getProduct(request, id):
   # ProductID = #request.query_params.get('id')#request.data.get('product_id')
    try:       
        product = Products.objects.get(id=id)
        serialized_Product = ProductsSerializer(product)
        return Response(serialized_Product.data, status=200)
    except:
        return Response({"Error - This Product Doesn’t Exist"}, status=400)
    
#Add New Product
@api_view(['GET', 'POST'])
def createProduct(request):
    product = request.data
    serialized_Product = ProductsSerializer(data=product)
    if (serialized_Product.is_valid()):
        serialized_Product.save()
        return Response(serialized_Product.data,status=201)
    else:
        return Response(serialized_Product.errors, status=400)

#Update Existing Product
@api_view(['PUT'])
def updateProduct(request, id):
    #ProductID = request.data.get('product_id')
    # newproduct_name = request.data.get('product_name')
    # newdescription = request.data.get('product_description')
    # newproduct_quantity = request.data.get('product_quantity')
    # newproduct_image = request.data.get('product_image')
    
    
    try:
        product = Products.objects.get(id=id)
        for key, value in request.POST.items():
              setattr(product, key, value)
        serialized_Product = ProductsSerializer(product)
        product.save()
        # product.product_name = newproduct_name
        # product.product_description = newdescription
        # product.product_quantity = newproduct_quantity
        # product.product_image = newproduct_image
        # serialized_Product = ProductsSerializer(product)
        # product.save()
        return Response(serialized_Product.data, status=200)
    except:
        return Response({"Error - This Product Doesn’t Exist"}, status=400)
    
#Delete Existing Product
@api_view(['DELETE'])
def deleteProduct(request, id):
   # ProductID = request.data.get('product_id')
    try:
        product = Products.objects.get(id=id)
        product.delete()
        return Response('{} is deleted'.format(product))
        #return Response({`$productProduct Deleted`},status=200)
    except:
        return Response({"Error - This Product Doesn’t Exist"}, status=400)

#Search For Products With Name
@api_view(['GET'])
def searchProduct(request, name):
    matchedProducts = Products.objects.filter(product_name=name)
    matchedProductsSerialized=ProductsSerializer(matchedProducts,many=True)
    return Response(matchedProductsSerialized.data, status=200)
 
# @api_view(['GET'])
# def all_products(request,name):  
#     product=Products.objects.filter(
#         product_name=name
#     )   
#     serializer=ProductsSerializer(product,many=True)
#     data = [{'product_image': item['product_image'], 'product_name': item['product_name'] , 'product_quantity' : item['product_quantity']} for item in serializer.data]
#     print(serializer.data[1]['id' ])
#     return Response(data)


"""----------------------------------------------------------------------- """



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
    

