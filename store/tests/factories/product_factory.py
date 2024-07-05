from decimal import Decimal
import random
import factory
import faker_commerce
from faker import Faker
from store.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile
from store.tests.factories.store_factory import StoreFactory


faker: Faker = Faker()
faker.add_provider(faker_commerce.Provider)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda _: faker.ecommerce_name())
    rating = factory.Faker("pyint")
    price = factory.Sequence(lambda _: Decimal(random.randint(1, 10)))
    description = factory.Faker("text")
    image = SimpleUploadedFile(
        name="test_image.jpeg",
        content=open("media/tests/test_file.png", "rb").read(),
        content_type="image/jpeg",
    )

    store = factory.SubFactory(StoreFactory)
