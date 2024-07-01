from django.http import HttpRequest, JsonResponse
from django.test import Client, TestCase, RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from store.views import add_to_bag

class AddToBagView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.session_store = SessionStore()

    def request_generator(self, product_id: int):
        request: HttpRequest = self.factory.post('/add-to-bag/', {'product_id': product_id})
        request.session: SessionStore = self.session_store
        return request

    def test_request_succeeds_when_product_quantity_is_one(self):
        response = add_to_bag(self.request_generator(1))
        self.assertJSONEqual(response.content, {'status': 'success', 'total_items': 1})

    def test_request_rejects_bad_product_id(self):
        with self.assertRaises(ValueError):
            add_to_bag(self.request_generator('bad id'))

    def test_request_increments_product_quantity(self):
        session = self.client.session
        session['bag'] = [{'product_id': 1, 'quantity': 1}]
        session.save()

        response: JsonResponse = self.client.post(reverse('store:add-to-bag'), {'product_id': 1})
        self.assertEqual(response.status_code, 200)

        bag: list = self.client.session['bag'] # Fetch the updated session data
        product_in_bag: dict = next((item for item in bag if item['product_id'] == 1), None)

        self.assertIsNotNone(product_in_bag, 'The product should exist in the bag')
        self.assertEqual(product_in_bag['quantity'], 2, "The quantity for this product should've been incremented.")