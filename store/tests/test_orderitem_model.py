from decimal import Decimal
from django.forms import ValidationError
from django.test import TestCase

from django.db.models import Q

from store.models import Order, OrderItem, Product

import random

from store.tests.utils import create_products


class TestOrderItem(TestCase):
    def setUp(self):
        self.products = create_products(10)
        self.bag = [{'product_id': product.id, 'quantity': 1} for product in self.products]

        self.client.session['bag'] = self.bag
        self.client.session.save()

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

    def test_product_quantity_successfully_associates_with_an_order(self):
        """
        Asserts that for each product specified in an order, 
        there exists exactly one corresponding record in the database 
        that matches both the product ID and the quantity associated with it in the order.
        This ensures not only the correct association of products to the order but 
        also verifies that each product is added with the precise quantity specified, 
        without duplication or omission.
        """
        for item in self.bag:
            product = Product.objects.get(id=int(item['product_id']))
            self.order.products.add(product)
            OrderItem.objects.create(order=self.order, product=product, quantity=item['quantity'])
        
        for item in self.bag:
            product_id = int(item['product_id'])
            quantity = item['quantity']
            matching_item = self.order.products.filter(
                    Q(id=product_id) & Q(orderitem__quantity=quantity)
                ).distinct()
            self.assertEqual(matching_item.count(), 1, f"Expected exactly one instance of product {matching_item} with quantity {quantity} in the order")

    def test_product_quantity_cannot_be_zero(self):
        bag = [{'product_id': product.id, 'quantity': 0} for product in self.products]
        
        for item in bag:
            with self.assertRaises(ValidationError):
                product = Product.objects.get(id=int(item['product_id']))
                OrderItem.objects.create(order=self.order, product=product, quantity=item['quantity'])