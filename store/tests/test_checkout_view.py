from django.test import Client, TestCase
from django.urls import reverse

from store.models import Order


class TestCheckoutView(TestCase):
    def setUp(self):
        self.client = Client()
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
                            "email": "michael@hotmail.com",
                            "phone_number": "(875) 844-6600",
                            "street": "7762 Newman Flats Suite 388",
                            "zip": "24306",
                            "city": "New Cindychester",
                            "state": "Pennsylvania"}
        
        response = self.client.post(reverse('store:checkout'), bad_form_data)
        form = response.context['form']

        self.assertFormError(form, 'first_name', 'This field is required.')
        self.assertFormError(form, 'last_name', 'This field is required.')
        self.assertFormError(form, 'phone_number', 'Please use XXX-XXX-XXXX format.')
        