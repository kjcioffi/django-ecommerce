import random
import string
from decimal import Decimal
from django.forms import ValidationError
from django.test import TestCase

from store.models import Product


class ProductModel(TestCase):
    def setUp(self):
        self.letters = string.ascii_lowercase
        self.product_name = ''.join(random.choice(self.letters) for _ in range(100))
        self.product = Product(name=self.product_name,
                               rating=0,
                               price=Decimal('10.99'),
                               description="Test")

    def validate_rating(self, rating: int, should_pass: bool):
        self.product.rating = rating
        if should_pass:
            try:
                self.product.full_clean()
            except ValidationError as e:
                self.assertNotIn('rating', e.message_dict)
        else:
            with self.assertRaises(ValidationError) as e:
                self.product.full_clean()
            self.assertIn('rating', e.exception.message_dict)

    def test_rating_below_minimum(self):
        self.validate_rating(-1, False)

    def test_rating_above_maximum(self):
        self.validate_rating(11, False)

    def test_rating_at_minimum(self):
        self.validate_rating(0, True)

    def test_rating_at_maximum(self):
        self.validate_rating(10, True)