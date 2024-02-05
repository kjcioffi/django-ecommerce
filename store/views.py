from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods

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


@require_http_methods(["POST"])
def add_to_bag(request) -> JsonResponse:
    """
    Process information from client-side interactions.

    Keeps count of the product itself and total quantity of each.
    """
    product_id = request.POST.get("product_id")

    bag = request.session.get('bag', [])

    for product in bag:
        if product['product_id'] == product_id:
            product['quantity'] += 1
            break
    else:
        bag.append({'product_id': product_id, 'quantity': 1})

    request.session['bag'] = bag

    total_items = sum(item['quantity'] for item in request.session['bag'])
    request.session['total_items'] = total_items
    
    return JsonResponse({'status': 'success', 'total_items': total_items})