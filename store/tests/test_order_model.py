from django.forms import ValidationError
from django.test import TestCase
from store.models import Product, Order


class OrderModel(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='Product 1',
            rating=8,
            price=19.99,
            description='Description for Product 1'
        )

        self.product2 = Product.objects.create(
            name='Product 2',
            rating=7,
            price=15.99,
            description='Description for Product 2',
        )

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

        self.invalid_phone_number = '+1555-555-5555'
        self.invalid_order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone_number=self.invalid_phone_number,
            street='123 Main St',
            zip='12345',
            city='Cityville',
            state='State'
        )

    def test_add_products_to_order(self):
        self.order.products.add(self.product1, self.product2)

        self.assertIn(self.product1, self.order.products.all())
        self.assertIn(self.product2, self.order.products.all())

    def test_remove_products_to_order(self):
        self.order.products.add(self.product1, self.product2)
        self.order.products.remove(self.product1)

        self.assertIn(self.product2, self.order.products.all())

    def test_query_products_in_order(self):
        self.order.products.add(self.product1, self.product2)

        product_in_order = Order.objects.filter(products=self.product1)
        self.assertTrue(product_in_order.exists())

    def test_valid_phone_number(self):
        phone_regex = r'^\d{3}-\d{3}-\d{4}$'
        self.assertRegex(self.order.phone_number, phone_regex)

    def test_invalid_phone_number(self):
        phone_regex = r'^\d{3}-\d{3}-\d{4}$'
        self.assertNotRegex(self.invalid_order.phone_number, phone_regex)
