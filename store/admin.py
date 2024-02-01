from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "rating", "price", "description", "image"]
