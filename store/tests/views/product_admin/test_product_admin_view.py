from django.test import TestCase
from django.urls import reverse

from store.tests.factories.product_factory import ProductFactory
from store.tests.factories.store_factory import StoreFactory
from store.tests.factories.user_factory import UserFactory


class TestProductAdminView(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.correct_store = StoreFactory(owner=self.owner)
        self.other_stores = StoreFactory.create_batch(10, owner=self.owner)
        self.products = ProductFactory.create_batch(10, store=self.correct_store)

    def test_admin_loads_first_store_when_multiple_owned(self):
        self.client.login(username=self.owner.username, password="")
        response = self.client.get(reverse("store:product_admin"))
        self.assertEqual(response.status_code, 200)
        store = response.context["store"]
        self.assertEqual(store, self.correct_store)
        products = list(store.product_set.all())
        self.assertEqual(products, self.products)
