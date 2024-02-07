from django.test import Client, TestCase, RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from store.views import add_to_bag

class AddToBagView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.session = SessionStore()

    def test_request_succeeds_when_product_quantity_is_one(self):
        request = self.factory.post('/add-to-bag/', {'product_id': 1})
        request.session = self.session
        response = add_to_bag(request)
        self.assertJSONEqual(response.content, {'status': 'success', 'total_items': 1})

    
        
        

    
