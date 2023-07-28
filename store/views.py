from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet ##Can also have ReadOnlyModelViewSet! no writing.
from rest_framework.views import APIView
from .models import Product, Collection,OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
         return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    # def destroy(self, request, pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
            return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(id=kwargs['pk']).count() > 0:
            return Response({'error': "collection cannot be deleted because it is associated with a product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def destroy(self, request, pk):
    #     collection = get_object_or_404(Collection,pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': "collection cannot be deleted because it is associated with a product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#CLASS-BASED VIEW WITH GENERICS
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     #can override get queryset and get serializer class with logic (e.g., permissions)
#     #instead of the two lines above - otherwise, just keep it simple :) 
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request':self.request}
    
#CLASS-BASED VIEW
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

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

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     #could do this instead of changing urls.py if we really wanna keep id
#     # lookup_field="id"
#     def delete(self, request, pk):
#         product = get_object_or_404(Product,pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class ProductDetail(APIView):
#     # product = get_object_or_404(Product,pk=id)
#     def get(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': "product cannot be deleted because it is associated with an order item."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

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



# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
#     def get_serializer_context(self):
#             return {'request':self.request}
    
#old version
#@api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == "GET":
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         #queryset = Collection.objects.all()#.prefetch_related('product_set').annotate(products_count=Count("product"))
#         serializer = CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         serializer.validated_data
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     # if request.method == 'GET':
#     #     queryset = Product.objects.select_related('collection').all()
#     #     serializer = ProductSerializer(queryset, many=True,context={'request': request})
#     #     return Response(serializer.data)
#     # elif request.method == 'POST':
#     #     serializer = ProductSerializer(data = request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     serializer.validated_data
#     #     return Response(serializer.data,status=status.HTTP_201_CREATED)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer
#     #could do this instead of changing urls.py if we really wanna keep id
#     # lookup_field="id"
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection,pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': "collection cannot be deleted because it is associated with a product"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count('products')),
#         pk=pk
#         )
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response({'error': "product cannot be deleted because it is associated with a product."},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     #return Response('ok')