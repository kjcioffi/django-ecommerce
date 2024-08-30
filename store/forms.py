from django import forms
from store.models import Order, Product, Store

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


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

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = "form-horizontal"
        self.helper.layout = Layout(
            Field("first_name", id="first_name", placeholder="First Name"),
            Field("last_name", id="last_name", placeholder="Last Name"),
            Field("email", id="email", placeholder="Email"),
            Field("phone_number", id="phone_number", placeholder="Phone Number"),
            Field("street", id="street", placeholder="Street"),
            Field("city", id="city", placeholder="City"),
            Field("state", id="state", placeholder="State"),
            Field("zip", id="zip", placeholder="Zip"),
            Submit("place-order", "Place Order", id="place-order"),
        )


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["store"]

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_class = "form-horizontal"
        self.helper.layout = Layout(
            Field("name", id="name", placeholder="Name"),
            Field("rating", id="rating", placeholder="Rating"),
            Field("price", id="price", placeholder="Price"),
            Field("description", id="description", placeholder="Description"),
            Field("image", id="image", placeholder="Image"),
            Submit("add-product", "Add Product", id="add-product"),
        )


class OrderAdminForm(forms.ModelForm):
    total_cost = forms.DecimalField(widget=forms.NumberInput(attrs={"readonly": True}))

    class Meta:
        model = Order
        exclude = ["store", "products"]
