import factory
from store.models import Store
from store.tests.factories.user_factory import UserFactory


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker("company")
    owner = factory.SubFactory(UserFactory)
    city = factory.Faker("city")
    state = factory.Faker("state")
