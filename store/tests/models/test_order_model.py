from decimal import Decimal
from django.test import TestCase
from store.models import Product, Order
from store.tests.utils import create_products


class TestOrderModel(TestCase):
    def setUp(self):
        self.invalid_phone_number = '+1555-555-5555'
        self.valid_phone_number = '555-555-5555'
        
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number=self.valid_phone_number,
            street='123 Main St',
            zip='12345',
            city='Cityville',
            state='State'
        )

        self.phone_regex = r'^\d{3}-\d{3}-\d{4}$'

        self.products = create_products(10)
        self.bag = [{'product_id': product.id, 'quantity': 1} for product in self.products]

        self.client.session['bag'] = self.bag
        self.client.session.save()
        
    def test_add_products_to_order(self):
        for product in self.products:
            self.order.products.add(product)
            self.assertIn(product, self.order.products.all())

    def test_remove_products_to_order(self):
        for product in self.products:
            self.order.products.add(product)
 
        product_to_be_removed = self.order.products.get(name__icontains="0")
        self.order.products.remove(product_to_be_removed)
        self.assertNotIn(product_to_be_removed, self.order.products.all())

    def test_query_products_in_order(self):
        for product in self.products:
            self.order.products.add(product)

        product_in_order = Order.objects.filter(products__name__icontains="3")
        self.assertTrue(product_in_order.exists())

    def test_valid_phone_number(self):
        self.assertRegex(self.order.phone_number, self.phone_regex)

    def test_invalid_phone_number(self):
        self.order.phone_number = self.invalid_phone_number
        self.assertNotRegex(self.order.phone_number, self.phone_regex)

    def test_products_associated_with_order(self):
        """
        Test that products added to a simulated bag are correctly associated with an order.    
        """
        for item in self.bag:
            product = Product.objects.get(id=int(item['product_id']))
            self.order.products.add(product)

        for item in self.bag:
            self.assertTrue(self.order.products.filter(id=int(item['product_id'])).exists(), f"Product {item['product_id']} should associated with this order.")

        self.assertEqual(len(self.bag), self.order.products.count(), "The number of products in this order should match the bag's contents")