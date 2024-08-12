from django.test import TestCase
from django.urls import reverse
from faker import Faker
import faker_commerce
from django.core.files.uploadedfile import SimpleUploadedFile

from store.models import Store
from store.tests.factories.user_factory import UserFactory

faker: Faker = Faker()
faker.add_provider(faker_commerce.Provider)


class CreateStoreViewTest(TestCase):

    def setUp(self):
        self.owner = UserFactory()

        self.client.login(username=self.owner.username, password="")

        self.data = {
            "name": faker.company(),
            "category": faker.ecommerce_category(),
            "city": faker.city(),
            "state": faker.state(),
            "image": SimpleUploadedFile(
                        name="test_image.jpeg",
                        content=open("media/tests/test_file.png", "rb").read(),
                        content_type="image/jpeg",
                    )
        }

        self.response = self.client.post(reverse("store:create_store"), data=self.data)

    def test_create_store_success(self):
        self.assertEqual(self.response.status_code, 302)
        store = Store.objects.for_user_admin(self.owner)
        self.assertTrue(store)
    
    def test_redirected_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("store:create_store"))
        self.assertEqual(response.status_code, 302)

    def test_store_created_with_no_image_provided(self):
        self.data["image"] = ""
        response = self.client.post(reverse("store:create_store"), data=self.data)
        self.assertEqual(response.status_code, 302)
