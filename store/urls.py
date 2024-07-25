from django.urls import path
from .views import (
    DownloadCustomerReport,
    DownloadProductReport,
    OrderAdmin,
    StoreList,
    StoreProducts,
    ProductDetail,
    ProductAdmin,
    ProductAdminAdd,
    checkout,
    add_to_bag,
    order_admin_modify,
    product_admin_modify,
)

app_name = "store"
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
    path(
        "user-admin/store/products/add",
        ProductAdminAdd.as_view(),
        name="product_admin_add",
    ),
    path("user-admin/store/orders", OrderAdmin.as_view(), name="order_admin"),
    path(
        "user-admin/store/order/modify/<int:pk>",
        order_admin_modify,
        name="order_admin_modify",
    ),
    path(
        "user-admin/reports/customers/csv",
        DownloadCustomerReport.as_view(),
        name="download_customer_report"
    ),
    path(
        "user-admin/reports/products",
        DownloadProductReport.as_view(),
        name="download_product_report"
    ),
]
