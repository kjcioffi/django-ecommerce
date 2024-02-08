from django import forms

from store.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["products"]