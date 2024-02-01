import random
import string
from decimal import Decimal
from django.forms import ValidationError
from django.test import TestCase

from store.models import Product


class ProductModel(TestCase):
    def setUp(self):
        self.letters = string.ascii_lowercase
        self.product = Product(name=''.join(random.choice(self.letters) for _ in range(100)),
                               rating=3,
                               price=Decimal('10.99'),
                               description="Test")

    def test_rating_rejects_integers_outside_of_the_range_of_0_and_10(self):
        self.product.rating = 12

        with self.assertRaises(ValidationError) as e:
            self.product.full_clean()

        self.assertIn('rating', e.exception.message_dict)

    def test_rating_accepts_integers_between_0_and_10(self):
        try:
            self.product.full_clean()
            self.product.rating = '7'
            self.product.full_clean()
        except ValidationError as e:
            self.assertNotIn('rating', e.message_dict)
