from django.test import TestCase, Client
from django.urls import reverse

from store.models import Product

class IndexView(TestCase):

    def create_product(self):
        return Product.objects.create(name="Test Product", rating=6, price=9.99, description="Testing")

    def test_max_six_products_populated(self):
        client = Client()
        response = client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)

        for _ in range(0, 10):
            self.create_product()

        response_queryset = response.context["product_list"]
        self.assertLessEqual(response_queryset.count(), 6)
        