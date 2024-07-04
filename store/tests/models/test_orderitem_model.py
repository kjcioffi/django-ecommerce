from django.forms import ValidationError
from django.test import TestCase

from django.db.models import Q

from store.models import Product


from store.tests.factories.order_factory import OrderFactory
from store.tests.factories.order_item_factory import OrderItemFactory


class TestOrderItem(TestCase):
    def setUp(self):
        self.order = OrderFactory()
        self.order_items = OrderItemFactory.create_batch(10, order=self.order)

        self.bag = [
            {"product_id": order_item.product.id, "quantity": order_item.quantity}
            for order_item in self.order_items
        ]

        self.client.session["bag"] = self.bag
        self.client.session.save()

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
            product_id = item["product_id"]
            quantity = item["quantity"]
            matching_item = self.order.products.filter(
                Q(id=product_id) & Q(orderitem__quantity=quantity)
            ).distinct()
            self.assertEqual(
                matching_item.count(),
                1,
                f"Expected exactly one instance of product {matching_item} with quantity {quantity} in the order",
            )

    def test_product_quantity_cannot_be_zero(self):
        bag = [
            {"product_id": product.id, "quantity": 0} for product in self.order_items
        ]

        for item in bag:
            with self.assertRaises(ValidationError):
                product = Product.objects.get(id=int(item["product_id"]))
                OrderItemFactory(
                    order=self.order, product=product, quantity=item["quantity"]
                )
