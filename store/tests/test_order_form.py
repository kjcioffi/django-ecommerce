import pdb
from django.forms import ValidationError
from django.test import TestCase

from store.forms import OrderForm

class TestOrderForm(TestCase):
    def setUp(self):
        self.form_data = {'first_name': 'Kevin', 'last_name': 'C', 'email': 'kc@example.com',
                                  'phone_number': '555-555-5555', 'street': 'Test St.', 'zip': '12345',
                                  'city': 'Test City', 'state': 'Testimonial'}

    def test_order_form_invalid(self):
        self.form_data['last_name'] = ''
        form = OrderForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_order_form_valid(self):
        form = OrderForm(self.form_data)
        self.assertTrue(form.is_valid())
    
    def test_phone_number_field_invalid(self):
        self.form_data['phone_number'] = '(555) 555-5555'
        form = OrderForm(self.form_data)
        self.assertFormError(form, 'phone_number', 'Please use XXX-XXX-XXXX format.')