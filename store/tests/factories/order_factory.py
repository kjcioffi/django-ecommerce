from decimal import Decimal
import random
import factory

from store.models import Order
from store.tests.factories.store_factory import StoreFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    store = factory.SubFactory(StoreFactory)
    total_cost = 0
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    street = factory.Faker("street_address")
    zip = factory.Faker("zip")
    city = factory.Faker("city")
    state = factory.Faker("state")
