from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from store.models import Order, Product, Store


class CreateStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(CreateStoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = "form-horizontal"
        self.helper.layout = Layout(
            Field("name", placeholder="Store Name"),
            Field("category", placeholder="Category"),
            Field("city", placeholder="City"),
            Field("state", placeholder="State"),
            Field("image", placeholder="Test"),
            Submit("create-store", "Create Store"),
        )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["store", "products", "total_cost", "paid_on"]


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["store"]


class OrderAdminForm(forms.ModelForm):
    total_cost = forms.DecimalField(widget=forms.NumberInput(attrs={"readonly": True}))

    class Meta:
        model = Order
        exclude = ["store", "products"]
