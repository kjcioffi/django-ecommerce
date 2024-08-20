from django.urls import path
from .views import (
    CreateStore,
    DownloadCustomerPDFReport,
    DownloadCustomerReport,
    DownloadProductPDFReport,
    DownloadProductReport,
    DownloadSalesPDFReport,
    DownloadSalesReport,
    OrderAdmin,
    StoreList,
    StoreProducts,
    ProductDetail,
    ProductAdmin,
    ProductAdminAdd,
    checkout,
    add_to_bag,
    create_payment_session,
    order_admin_modify,
    product_admin_modify,
    stripe_webhook,
)

app_name = "store"
urlpatterns = [
    path("create-store", CreateStore.as_view(), name="create_store"),
    path("store/<int:store_id>", StoreProducts.as_view(), name="store_front"),
    path("", StoreList.as_view(), name="store_list"),
    path("store/product/<int:pk>", ProductDetail.as_view(), name="product"),
    path("checkout/", checkout, name="checkout"),
    path(
        "create-payment-session", create_payment_session, name="create_payment_session"
    ),
    path("stripe-webhook", stripe_webhook, name="stripe_webhook"),
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
        name="download_customer_report",
    ),
    path(
        "user-admin/reports/customers/pdf",
        DownloadCustomerPDFReport.as_view(),
        name="download_customer_pdf_report",
    ),
    path(
        "user-admin/reports/products",
        DownloadProductReport.as_view(),
        name="download_product_report",
    ),
    path(
        "user-admin/reports/products/pdf",
        DownloadProductPDFReport.as_view(),
        name="download_product_pdf_report",
    ),
    path(
        "user-admin/reports/sales",
        DownloadSalesReport.as_view(),
        name="download_sales_report",
    ),
    path(
        "user-admin/reports/sales/pdf",
        DownloadSalesPDFReport.as_view(),
        name="download_sales_pdf_report",
    ),
]
