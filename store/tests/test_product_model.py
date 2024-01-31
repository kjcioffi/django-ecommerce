import random
import string
from decimal import Decimal
from django.forms import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from store.models import Product


class ProductModel(TestCase):
    def setUp(self):
        self.letters = string.ascii_lowercase
        self.product = Product(name=''.join(random.choice(self.letters) for _ in range(100)),
                               rating=3,
                               price=Decimal('10.99'),
                               description="Test")

    def test_name_rejects_over_100_chars(self):
        self.product.name += '*'
        
        with self.assertRaises(ValidationError) as e:
            self.product.full_clean()

        self.assertIn('name', e.exception.message_dict)

    def test_name_accepts_100_chars(self):
        try:
            self.product.full_clean()
        except ValidationError as e:
            self.assertNotIn('name', e.message_dict)

    def test_name_rejects_empty_string(self):
        self.product.name = ''

        with self.assertRaises(ValidationError) as e:
            self.product.full_clean()

        self.assertIn('name', e.exception.message_dict)