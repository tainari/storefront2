# from django.urls import path
# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers #needs pipenv install drf-nested-routers
from . import views
from pprint import pprint


# router = SimpleRouter()
router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
urlpatterns = router.urls + products_router.urls
#DefaultRouter 
###ORRRRRR..... if you have other ones that you need to include
# urlpatterns = [
#     path('',include(router.urls))
# ]


# URLConf
# urlpatterns = [
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail')
#     # path('collections/<int:pk>/', views.collection_detail,name='collection-detail')
# ]
