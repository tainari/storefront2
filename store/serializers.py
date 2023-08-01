from decimal import Decimal
from django.db.models import Count
from rest_framework import serializers
from .models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    products_count = serializers.IntegerField(read_only=True)
        #did this unnecessarily - can put it in the GET method
        #fields = ['id','title','num_products']
    # num_products = serializers.SerializerMethodField(method_name="ct_products")

    # def ct_products(self,collection: Collection):
    #     #can use .product here because it's the related_name in the Product model FOreign Key 
    #     return collection.product.count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
        #note - collection gives default; if you want something different,
        #uncomment one of the collection = options below
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2,source="unit_price")
    # price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # #option 1 - primary key
    # # collection = serializers.PrimaryKeyRelatedField(
    # #     queryset = Collection.objects.all()
    # # )
    # #option 2 - string value; just returns name (overridden __str__ method in models)
    # #collection = serializers.StringRelatedField()
    # #OPTION 3 - nested object - collection returned as object 
    # # collection = CollectionSerializer()
    # #OPTION 4 - hyperlink - renders as hyperlink to view collection
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    

    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)
    
    ##SAVE METHOD WILL CALL ONE OF CREATE AND UPDATE DEPENDING ON THE STATE OF THE SERIALIZER
    # ##customize product creation
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    #     # return super().create(validated_data)

    # ##customize product update
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
    
    #EXAMPLE OF CUSTOM VALIDATION
    # def validate(self,data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)