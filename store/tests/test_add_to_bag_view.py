from django.http import HttpRequest
from django.test import Client, TestCase, RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from store.views import add_to_bag

class AddToBagView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.session = SessionStore()

    def request_generator(self, product_id: int):
        request: HttpRequest = self.factory.post('/add-to-bag/', {'product_id': product_id})
        request.session: SessionStore = self.session
        return request

    def test_request_succeeds_when_product_quantity_is_one(self):
        response = add_to_bag(self.request_generator(1))
        self.assertJSONEqual(response.content, {'status': 'success', 'total_items': 1})

    def test_request_rejects_bad_product_id(self):
        with self.assertRaises(ValueError):
            add_to_bag(self.request_generator('bad id'))


    
        
        

    
