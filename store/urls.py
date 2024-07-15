from django.urls import path
from .views import StoreList, StoreProducts, ProductDetail, ProductAdmin, checkout, add_to_bag

app_name = 'store'
urlpatterns = [
    path("user-admin/store/products", ProductAdmin.as_view(), name="product_admin"),
]
