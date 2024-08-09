from django.test import TestCase
from django.urls import reverse
from faker import Faker

from store.models import Order
from store.tests.factories.order_item_factory import OrderItemFactory
from store.tests.factories.product_factory import ProductFactory
from store.tests.factories.store_factory import StoreFactory

faker = Faker()


class TestCheckoutView(TestCase):
    def setUp(self):
        # Create first store and it's products
        self.store1 = StoreFactory()

        self.store1_products = ProductFactory.create_batch(5, store=self.store1)
        self.bag_items = []

        for product in self.store1_products:
            self.bag_items.append(OrderItemFactory(product=product))

        # Create other store
        self.store2 = StoreFactory()

        self.store2_products = ProductFactory.create_batch(1, store=self.store2)

        for product in self.store2_products:
            self.bag_items.append(OrderItemFactory(product=product))

        # Initialize session and simulate bag
        self.session = self.client.session
        self.session["bag"] = [
            {"product_id": bag_item.product.id, "quantity": bag_item.quantity}
            for bag_item in self.bag_items
        ]
        self.session.save()

        # initialize data for form submission
        self.form_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "phone_number": faker.basic_phone_number(),
            "street": faker.street_address(),
            "zip": faker.zipcode(),
            "city": faker.city(),
            "state": faker.state(),
        }

        self.response = self.client.get(reverse("store:checkout"))

    def test_form_display(self):
        self.assertEqual(self.response.status_code, 200)
        form = self.response.context["form"]
        self.assertTrue(form)

    def test_form_submit_success(self):
        request = self.post_form_data(self.form_data)
        self.assertEqual(request.status_code, 302)

    def test_form_submit_fails_with_field_errors(self):
        bad_form_data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone_number": "",
            "street": "",
            "zip": "",
            "city": "",
            "state": "",
        }

        request = self.post_form_data(bad_form_data)
        form = request.context["form"]

        self.assertFormError(form, "first_name", "This field is required.")
        self.assertFormError(form, "last_name", "This field is required.")
        self.assertFormError(form, "street", "This field is required.")
        self.assertFormError(form, "zip", "This field is required.")
        self.assertFormError(form, "city", "This field is required.")
        self.assertFormError(form, "state", "This field is required.")

    def test_quantities_in_context_match_up_with_session(self):
        self.assertEqual(self.response.status_code, 200)

        session_bag_product_quantities: dict = {
            item["product_id"]: item["quantity"] for item in self.session["bag"]
        }

        for product_in_context in self.response.context["products_in_bag"]:
            product_id = product_in_context["product"].id
            product_quantity = product_in_context["quantity"]

            self.assertIn(
                product_id,
                session_bag_product_quantities,
                f"Product ID {product_id} wasn't found in bag items.",
            )
            self.assertEqual(
                product_quantity, session_bag_product_quantities[product_id]
            )

    def test_checkout_view_with_empty_session(self):
        self.session["bag"] = []
        self.session.save()

        response_with_updated_session = self.client.get(reverse("store:checkout"))

        self.assertEqual(response_with_updated_session.status_code, 200)
        self.assertEqual(response_with_updated_session.context["products_in_bag"], [])

    def test_session_total_equals_context_total(self):
        # products_in_bag context item maps the necessary session data and product model objects needed.
        session_total = sum(
            bag_item["product"].price * bag_item["quantity"]
            for bag_item in self.response.context["products_in_bag"]
        )

        self.assertEqual(session_total, self.response.context["total_cost"])

    def post_form_data(self, form_data):
        return self.client.post(reverse("store:checkout"), form_data)
