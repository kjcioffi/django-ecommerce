from django.urls import path
from .views import *

app_name = 'store'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product'),
    path('add-to-bag/', add_to_bag, name='add-to-bag'),
]
