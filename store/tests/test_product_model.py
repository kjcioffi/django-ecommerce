import random
import string
from django.forms import ValidationError
from django.test import TestCase

from store.models import Product


class ProductModel(TestCase):
    def test_name_rejects_over_100_chars(self):
        letters = string.ascii_lowercase
        product = Product(name=''.join(random.choice(letters) for _ in range(101)))
        
        with self.assertRaises(ValidationError) as full_clean:
            product.full_clean()

        self.assertIn('name', full_clean.exception.message_dict)