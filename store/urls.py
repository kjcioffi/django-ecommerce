from django.urls import path
from .views import Index, ProductDetail, ProductAdmin, checkout, add_to_bag

app_name = 'store'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-bag/', add_to_bag, name='add-to-bag'),
    path('user-admin/products', ProductAdmin.as_view(), name='product_admin'),
]
