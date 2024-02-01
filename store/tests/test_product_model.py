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
