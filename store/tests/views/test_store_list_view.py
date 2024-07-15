from django.test import TestCase
from django.urls import reverse

from store.tests.factories.store_factory import StoreFactory

class StoreListView(TestCase):
    def setUp(self):
        self.stores = StoreFactory.create_batch(10)
        self.response = self.client.get(reverse('store:store_list'))

    def test_stores_in_context(self):
        
        self.assertEqual(self.response.status_code, 200)

        response_queryset = self.response.context["stores"]
        self.assertEqual(len(response_queryset), 10)
        