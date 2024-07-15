from django.urls import path
from .views import (
    StoreList,
    StoreProducts,
    ProductDetail,
    ProductAdmin,
    checkout,
    add_to_bag,
    product_admin_modify,
)

app_name = 'store'
urlpatterns = [
    path("store/<int:store_id>", StoreProducts.as_view(), name="store_front"),
    path("", StoreList.as_view(), name="store_list"),
    path("store/product/<int:pk>", ProductDetail.as_view(), name="product"),
    path("checkout/", checkout, name="checkout"),
    path("add-to-bag/", add_to_bag, name="add-to-bag"),
    path("user-admin/store/products", ProductAdmin.as_view(), name="product_admin"),
    path(
        "user-admin/store/products/modify/<int:pk>",
        product_admin_modify,
        name="product_admin_modify",
    ),
]
