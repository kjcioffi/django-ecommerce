from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from store.models import Product

class Index(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = 'store/index.html'

    def get_queryset(self) -> QuerySet[Product]:
        return super().get_queryset()[:6]
