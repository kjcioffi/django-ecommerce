import random
import factory

from store.models import OrderItem
from store.tests.factories.order_factory import OrderFactory
from store.tests.factories.product_factory import ProductFactory


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = factory.Sequence(lambda _: random.randint(1, 10))
