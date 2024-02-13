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
        self.session['bag'] = [{'product_id': product.id, 'quantity': random.randint(0, 10)} for product in self.products]
        self.session.save()

        self.form_data = {"first_name": "Michael",
                            "last_name": "Dillon",
                            "email": "donald74@hotmail.com",
                            "phone_number": "875-844-6600",
                            "street": "7762 Newman Flats Suite 388",
                            "zip": "24306",
                            "city": "New Cindychester",
                            "state": "Pennsylvania"}

    def test_form_display(self):
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form)

    def test_form_submit_success(self):
        response = self.client.post(reverse('store:checkout'), self.form_data)
        self.assertEqual(response.status_code, 302)
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
        
        response = self.client.post(reverse('store:checkout'), bad_form_data)
        form = response.context['form']

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
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)

        session_bag_product_quantities: dict = {item['product_id']: item['quantity'] for item in self.session['bag']}

        for product_in_context in response.context['products_in_bag']:
            product_id = product_in_context['product'].id
            product_quantity = product_in_context['quantity']

            self.assertIn(product_id, session_bag_product_quantities, f"Product ID {product_id} wasn't found in bag items.")
            self.assertEqual(product_quantity, session_bag_product_quantities[product_id])

    def test_checkout_view_with_empty_session(self):
        self.session['bag'] = []
        self.session.save()

        response = self.client.get(reverse('store:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products_in_bag'], [])
