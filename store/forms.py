from django import forms

from store.models import Order, Product

import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["store", "products", "total_cost"]


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["store"]
    