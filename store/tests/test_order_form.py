from decimal import Decimal
import random as rand

from django.test import TestCase, Client
from django.urls import reverse

from store.forms import OrderForm
from store.models import Order, Product

class TestOrderForm(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {'first_name': 'Kevin', 'last_name': 'C', 'email': 'kc@example.com',
                                  'phone_number': '555-555-5555', 'street': 'Test St.', 'zip': '12345',
                                  'city': 'Test City', 'state': 'Testimonial'}

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

    def test_products_associated_with_order(self):
        """
        Test that products added to a simulated bag are correctly associated with an order.    
        """
        for _ in range(0, 10):
            self.client.post(reverse('store:add-to-bag'), {'product_id': rand.randint(11, 19)})

        bag: list = self.client.session.get('bag', [])

        order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number='555-555-5555',
            street='123 Main St',
            zip='12345',
            city='Cityville',
            state='State'
        )

        self.create_products(10)

        for item in bag:
            product = Product.objects.get(id=int(item['product_id']))
            order.products.add(product)

        expected_product_ids: list = [item['product_id'] for item in bag]
        actual_product_ids: list = [product.id for product in order.products.all()]

        self.assertTrue(all(product_id in expected_product_ids for product_id in actual_product_ids), 'All products from the bag should be in the order.')
        self.assertEqual(len(bag), order.products.count(), 'All products from the bag should be in the order.')


    def create_products(self, number: int):
        for i in range(1, number):
            Product.objects.create(name=f"Product {i}",
                                rating=0,
                                price=Decimal('10.99'),
                                description="Test")