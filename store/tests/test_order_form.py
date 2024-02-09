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

        products = self.create_products(10)
        bag = [{'product_id': product.id, 'quantity': 1} for product in products]

        self.client.session['bag'] = bag
        self.client.session.save()

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

        for item in bag:
            product = Product.objects.get(id=int(item['product_id']))
            order.products.add(product)

        for item in bag:
            self.assertTrue(order.products.filter(id=int(item['product_id'])).exists(), f"Product {item['product_id']} should associated with this order.")

        self.assertEqual(len(bag), order.products.count(), "The number of products in this order should match the bag's contents")

    def test_product_quantities_associated_with_order(self):
        pass

    def create_products(self, quantity: int):
        products = []
        for i in range(quantity):
            product = Product.objects.create(
                name=f"Product {i}",
                rating=0,
                price=Decimal('10.99'),
                description="Test")
            products.append(product)
        return products