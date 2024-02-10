from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from store.forms import OrderForm

from store.models import Product

class Index(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = 'store/index.html'

    def get_queryset(self) -> QuerySet[Product]:
        return super().get_queryset()[:6]

class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'store/product_detail.html'


class Checkout(CreateView):
    form_class = OrderForm
    template_name = 'store/checkout.html'
    success_url = reverse_lazy('store:index')


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