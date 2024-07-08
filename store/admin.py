from django.contrib import admin

from .models import Order, OrderItem, Product, Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fields = ["owner", "name", "city", "state"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["store", "name", "rating", "price", "decription", "image"]


class OrderItemStackedInline(admin.StackedInline):
    model = OrderItem
    fields = ["product", "order", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = [
        "store",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "street",
        "zip",
        "city",
        "state",
    ]
    inlines = [OrderItemStackedInline]
