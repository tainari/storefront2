from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.

#CLASS-BASED VIEW
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.validated_data
        return Response(serializer.data,status=status.HTTP_201_CREATED)

#VIEW FUNCTION
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #or use this for lines starting with serializer.is_valid
        # if serializer.is_valid():
        #     serializer.validated_datas
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    # product = get_object_or_404(Product,pk=id)
    def get(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self,request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        product = get_object_or_404(Product,pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#     product = get_object_or_404(Product,pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if product.orderitem_set.count() > 0:
#             return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    ######
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        #queryset = Collection.objects.all()#.prefetch_related('product_set').annotate(products_count=Count("product"))
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.validated_data
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    # if request.method == 'GET':
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(queryset, many=True,context={'request': request})
    #     return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = ProductSerializer(data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     serializer.validated_data
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')),
        pk=pk
        )
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({'error': "product cannot be deleted because it is associated with a product."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #return Response('ok')