from django.http import HttpResponseForbidden
from django.test import TestCase
from django.urls import reverse

from store.tests.factories.product_factory import ProductFactory
from store.tests.factories.store_factory import StoreFactory
from store.tests.factories.user_factory import UserFactory

class TestProductAdminModifyView(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.correct_store = StoreFactory(owner=self.owner)
        self.product = ProductFactory(store=self.correct_store)
        self.customer = UserFactory()

    def test_customer_cannot_modify_products(self):
        self.client.login(username=self.customer.username, password="")

        response = self.client.get(reverse("store:product_admin_modify", kwargs={"pk": self.product.pk}))
        self.assertIsInstance(response, HttpResponseForbidden)