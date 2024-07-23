from django.http import HttpResponseForbidden
from django.test import TestCase
from django.urls import reverse

from store.tests.factories.order_factory import OrderFactory
from store.tests.factories.store_factory import StoreFactory
from store.tests.factories.user_factory import UserFactory

class TestProductAdminModifyView(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.correct_store = StoreFactory(owner=self.owner)
        self.order = OrderFactory(store=self.correct_store)
        self.customer = UserFactory()

    def test_customer_cannot_modify_products(self):
        self.client.login(username=self.customer.username, password="")

        response = self.client.get(reverse("store:order_admin_modify", kwargs={"pk": self.order.pk}))
        self.assertIsInstance(response, HttpResponseForbidden)