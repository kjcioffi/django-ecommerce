from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from store.forms import OrderForm, ProductAdminForm

from store.models import OrderItem, Product, Store
from django.contrib.auth.mixins import LoginRequiredMixin

class StoreProducts(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/store_products.html"

    def get_queryset(self) -> QuerySet[Product]:
        store_id = self.kwargs.get('store_id')
        queryset = Product.objects.filter(store=store_id)
        return queryset

class StoreList(ListView):
    model = Store
    context_object_name = "stores"
    template_name = "store/store_list.html"

class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'store/product_detail.html'

def checkout(request):

    # populate products in the purchase summary of the web page
    products_in_bag = get_products_and_quantities_from_bag(request)

    # context item for customer to view when placing order.
    total_cost = sum(bag_item["product"].price * bag_item["quantity"] for bag_item in products_in_bag)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            for bag_item in products_in_bag:
                OrderItem.objects.create(order=order, product=bag_item["product"], quantity=bag_item["quantity"])

            request.session['bag'] = []
            request.session['total_items'] = 0

            messages.add_message(request, messages.SUCCESS, "Order placed! Thank you for your business, "
                                "most customers recieve their orders in 2 - 3 business days. "
                                "Please contact us if it has been more than 5 business days.")
            
            return redirect('store:index')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {'form': form, 'products_in_bag': products_in_bag, 'total_cost': total_cost})

def get_products_and_quantities_from_bag(request):
    products = []
    if 'bag' in request.session:
        for product in request.session['bag']:
            product_instance = Product.objects.get(id=product['product_id'])
            products.append({
                'product': product_instance,
                'quantity': product['quantity'],
                'image': product_instance.image.url
                })
        return products
    else:
        return products
        

@require_http_methods(["POST"])
def add_to_bag(request) -> JsonResponse:
    """
    Process information from client-side interactions then \
    send the total number of items in the bag.

    Keeps count of different products added and their quantities.
    """
    product_id = int(request.POST.get("product_id"))

    if not isinstance(product_id, int):
        raise TypeError("Product ID must be an integer.")

    bag: list = request.session.get('bag', [])

    product_found = False
    for product in bag:
        if product['product_id'] == product_id:
            product['quantity'] += 1
            product_found = True
            break
    
    if not product_found:
        bag.append({'product_id': product_id, 'quantity': 1})

    request.session['bag'] = bag

    total_items = sum(product['quantity'] for product in bag)
    request.session['total_items'] = total_items

    return JsonResponse({'status': 'success', 'total_items': total_items})

class ProductAdmin(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/product_admin.html"
    login_url = "/accounts/login"

    def get_queryset(self) -> QuerySet[Product]:
        # return products only from the store they own
        return Product.objects.filter(store__owner=self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        context["store"] = self.request.user.store_set.get()
        return context
    
def product_modify_admin(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductAdminForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.add_message(f"{product.name}({product.pk}) successfully saved.")
            return redirect(reverse("store:product_admin"))
        else:
            form = ProductAdminForm()
    
    return render(request, 'store/product_admin_modify.html', {'form': form})
