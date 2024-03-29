from django.test import TestCase, Client

from store.forms import OrderForm
from store.models import Order

class TestOrderForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {'first_name': 'Kevin', 'last_name': 'C', 'email': 'kc@example.com',
                                  'phone_number': '555-555-5555', 'street': 'Test St.', 'zip': '12345',
                                  'city': 'Test City', 'state': 'Testimonial'}

        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number='555-555-5555',
            street='123 Main St',
            zip='12345',
            city='Cityville',
            state='State'
        )

    def test_order_form_invalid(self):
        self.form_data['last_name'] = ''
        form = OrderForm(self.form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid.")

    def test_order_form_valid(self):
        form = OrderForm(self.form_data)
        self.assertTrue(form.is_valid(), "The form should be valid.")
    
    def test_phone_number_field_invalid(self):
        self.form_data['phone_number'] = '(555) 555-5555'
        form = OrderForm(self.form_data)
        self.assertFormError(form, 'phone_number', 'Please use XXX-XXX-XXXX format.')

    def test_order_form_save(self):
        form = OrderForm(self.form_data)
        self.assertTrue(form.is_valid(), 'The form should be valid.')
        model_object = form.save()
        self.assertTrue(Order.objects.filter(pk=model_object.pk).exists(), 'The order object should exist in the database after saving.')