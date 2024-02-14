from django import forms

from store.models import Order

import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["products", "total_cost"]
        

    def clean_phone_number(self):
        pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
        phone_number: str = self.cleaned_data.get('phone_number')

        if not pattern.match(phone_number):
            raise forms.ValidationError('Please use XXX-XXX-XXXX format.')
        return phone_number