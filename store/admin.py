from django.contrib import admin

from .models import Product, Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fields = ["owner", "name", "city", "state"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "rating", "price", "description", "image"]
