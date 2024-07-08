from django.test import TestCase
from store.models import Product
from store.tests.factories.order_factory import OrderFactory
from store.tests.factories.order_item_factory import OrderItemFactory


class TestOrderModel(TestCase):
    def setUp(self):
        self.invalid_phone_number = "+1555-555-5555"
        self.valid_phone_number = "555-555-5555"

        self.order = OrderFactory()

        self.order_items = OrderItemFactory.create_batch(10, order=self.order)
        self.bag = [
            {"product_id": order_item.product.id, "quantity": order_item.quantity}
            for order_item in self.order_items
        ]

        self.client.session["bag"] = self.bag
        self.client.session.save()

    def test_add_products_to_order(self):
        """
        Ensure products are properly added to an order.
        """
        for order_item in self.order_items:
            self.order.products.add(order_item.product)
            self.assertIn(
                order_item.product,
                self.order.products.all(),
                f"Product {order_item.product.name} should've been added to the order.",
            )

    def test_remove_products_to_order(self):
        """
        Ensure products are properly removed from an order.
        """
        for order_item in self.order_items:
            self.order.products.add(order_item.product)

        product_to_be_removed = self.order.products.all()[0]
        self.order.products.remove(product_to_be_removed)
        self.assertNotIn(
            product_to_be_removed,
            self.order.products.all(),
            f"Product {order_item.product.name} should've been removed from the order.",
        )

    def test_products_associated_with_order(self):
        """
        Ensure products added to a simulated bag are correctly associated with an order.
        """
        for item in self.bag:
            product = Product.objects.get(id=item["product_id"])
            self.order.products.add(product)

        for item in self.bag:
            self.assertTrue(
                self.order.products.filter(id=item["product_id"]).exists(),
                f"Product {item['product_id']} should associated with this order.",
            )

        self.assertEqual(
            len(self.bag),
            self.order.products.count(),
            "The number of products in this order should match the bag's contents",
        )

    def test_total_cost_not_zero_when_product_added(self):
        """
        When OrderItems are added to an order, ensure they update the total cost of an order.
        """
        order = OrderFactory()
        order_items = OrderItemFactory.create_batch(10, order=order)
        order_total = sum([item.product.price * item.quantity for item in order_items])

        self.assertEqual(order_total, order.total_cost)
