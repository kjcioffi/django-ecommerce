import factory
from faker import Faker
import faker_commerce
from store.models import Store
from store.tests.factories.user_factory import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile


faker: Faker = Faker()
faker.add_provider(faker_commerce.Provider)


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker("company")
    owner = factory.SubFactory(UserFactory)
    category = factory.Sequence(lambda _: faker.ecommerce_category())
    city = factory.Faker("city")
    state = factory.Faker("state")
    image = SimpleUploadedFile(
        name="test_image.jpeg",
        content=open("media/tests/test_file.png", "rb").read(),
        content_type="image/jpeg",
    )
