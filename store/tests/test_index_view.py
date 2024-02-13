from django.test import TestCase, Client
from django.urls import reverse

from store.tests.utils import create_products

class IndexView(TestCase):
    def test_max_six_products_populated(self):
        client = Client()
        response = client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)

        create_products(1)

        response_queryset = response.context["product_list"]
        self.assertLessEqual(response_queryset.count(), 6)
        