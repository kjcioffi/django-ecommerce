import random
import string
from django.forms import ValidationError
from django.test import TestCase

from store.models import Product, Store
from store.tests.factories.product_factory import ProductFactory


class ProductModel(TestCase):
    def setUp(self):
        self.letters = string.ascii_lowercase
        self.product_name = "".join(random.choice(self.letters) for _ in range(100))
        self.product = ProductFactory()

    def validate_rating(self, rating: int, should_pass: bool):
        """
        A helper method to validate the product rating.

        :param int rating: product rating to validate
        :param bool should_pass: the expected result of the test
        """
        self.product.rating = rating
        if should_pass:
            try:
                self.product.full_clean()
            except ValidationError as e:
                self.assertNotIn("rating", e.message_dict)
        else:
            with self.assertRaises(ValidationError) as e:
                self.product.full_clean()
            self.assertIn("rating", e.exception.message_dict)

    def test_rating_below_minimum(self):
        self.validate_rating(-1, False)

    def test_rating_above_maximum(self):
        self.validate_rating(11, False)

    def test_rating_at_minimum(self):
        self.validate_rating(0, True)

    def test_rating_at_maximum(self):
        self.validate_rating(10, True)

    def test_store_delete_cascades_product(self):
        self.product.store.delete()
        self.assertNotIn(self.product, Product.objects.all())

    def test_product_doesnt_delete_cascade_store(self):
        self.product.delete()
        self.assertIn(self.product.store, Store.objects.all())
