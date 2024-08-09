from django import forms

from store.models import Order, Product, Store


class CreateStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ["owner"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["store", "products", "total_cost"]


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["store"]


class OrderAdminForm(forms.ModelForm):
    total_cost = forms.DecimalField(widget=forms.NumberInput(attrs={"readonly": True}))

    class Meta:
        model = Order
        exclude = ["store", "products"]
