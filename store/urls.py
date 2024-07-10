from django.urls import path
from .views import *

app_name = 'store'
urlpatterns = [
    path('store/<int:store_id>', StoreProducts.as_view(), name='store_front'),
    path('', StoreList.as_view(), name='store_list'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-bag/', add_to_bag, name='add-to-bag'),
]
