import random
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Order
from store.tests.utils import create_products


class TestCheckoutView(TestCase):
    def setUp(self):
        self.client = Client()

        self.products = create_products(10)

        self.session = self.client.session
        self.session['bag'] = [{'product_id': product.id, 'quantity': random.randint(1, 10)} for product in self.products]
        self.session.save()

        self.form_data = {"first_name": "Michael",
                            "last_name": "Dillon",
                            "email": "donald74@hotmail.com",
                            "phone_number": "875-844-6600",
                            "street": "7762 Newman Flats Suite 388",
                            "zip": "24306",
                            "city": "New Cindychester",
                            "state": "Pennsylvania"}
        
        self.response = self.client.get(reverse('store:checkout'))

    def test_form_display(self):
        self.assertEqual(self.response.status_code, 200)
        form = self.response.context['form']
        self.assertTrue(form)

    def test_form_submit_success(self):
        request = self.post_form_data(self.form_data)
        self.assertEqual(request.status_code, 302)
        saved_order = Order.objects.filter(first_name="Michael", last_name="Dillon")
        self.assertTrue(saved_order.exists())

    def test_form_submit_fails_with_field_errors(self):
        bad_form_data = {"first_name": "",
                            "last_name": "",
                            "email": "",
                            "phone_number": "",
                            "street": "",
                            "zip": "",
                            "city": "",
                            "state": ""}
        
        request = self.post_form_data(bad_form_data)
        form = request.context['form']

        self.assertFormError(form, 'first_name', 'This field is required.')
        self.assertFormError(form, 'last_name', 'This field is required.')
        self.assertFormError(form, 'street', 'This field is required.')
        self.assertFormError(form, 'zip', 'This field is required.')
        self.assertFormError(form, 'city', 'This field is required.')
        self.assertFormError(form, 'state', 'This field is required.')

        if bad_form_data['phone_number'] == "":
            self.assertFormError(form, 'phone_number', 'This field is required.')
        else:
            self.assertFormError(form, 'phone_number', 'Please use XXX-XXX-XXXX format.')

    def test_quantities_in_context_match_up_with_session(self):
        self.assertEqual(self.response.status_code, 200)

        session_bag_product_quantities: dict = {item['product_id']: item['quantity'] for item in self.session['bag']}

        for product_in_context in self.response.context['products_in_bag']:
            product_id = product_in_context['product'].id
            product_quantity = product_in_context['quantity']

            self.assertIn(product_id, session_bag_product_quantities, f"Product ID {product_id} wasn't found in bag items.")
            self.assertEqual(product_quantity, session_bag_product_quantities[product_id])

    def test_checkout_view_with_empty_session(self):
        self.session['bag'] = []
        self.session.save()

        response_with_updated_session = self.client.get(reverse('store:checkout'))

        self.assertEqual(response_with_updated_session.status_code, 200)
        self.assertEqual(response_with_updated_session.context['products_in_bag'], [])

    def test_session_total_equals_context_total(self):
        # products_in_bag context item maps the necessary session data and product model objects needed.
        session_total = sum(bag_item['product'].price * bag_item['quantity'] for bag_item in self.response.context['products_in_bag'])

        self.assertEqual(session_total, self.response.context['total_cost'])

    def test_order_total_persists_after_order_placed(self):
        request = self.post_form_data(self.form_data)
        self.assertEqual(request.status_code, 302)

        saved_order = Order.objects.filter(first_name="Michael", last_name="Dillon")
        self.assertTrue(saved_order.exists())
        saved_order = saved_order.get()

        self.assertEqual(saved_order.total_cost, self.response.context["total_cost"])

    def post_form_data(self, form_data):
        return self.client.post(reverse('store:checkout'), form_data)