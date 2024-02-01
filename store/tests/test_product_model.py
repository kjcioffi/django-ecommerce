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
                               rating=0,
                               price=Decimal('10.99'),
                               description="Test")

    def test_rating_below_minimum(self):
        self.product.rating = -1
        with self.assertRaises(ValidationError) as e:
            self.product.full_clean()
        
        self.assertIn('rating', e.exception.message_dict)

    def test_rating_above_maximum(self):
        self.product.rating = 11
        with self.assertRaises(ValidationError) as e:
            self.product.full_clean()
        
        self.assertIn('rating', e.exception.message_dict)

    def test_rating_at_minimum(self):
        try:
            self.product.full_clean()
        except ValidationError as e:
            self.assertNotIn('rating', e.message_dict)

    def test_rating_at_maximum(self):
        self.product.rating = 10
        try:
            self.product.full_clean()
        except ValidationError as e:
            self.assertNotIn('rating', e.message_dict)