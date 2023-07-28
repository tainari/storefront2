from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from pprint import pprint

router = SimpleRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
urlpatterns = router.urls
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
