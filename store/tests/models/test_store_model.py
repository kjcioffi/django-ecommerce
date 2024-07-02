import random
import string

from django.contrib.auth.models import User

from django.forms import ValidationError
from django.test import TestCase

from store.models import Store
from store.tests.factories.store_factory import StoreFactory


class TestStoreModel(TestCase):
    def setUp(self):
        self.name_char_length: int = Store._meta.get_field("name").max_length
        self.city_char_length: int = Store._meta.get_field("city").max_length
        self.state_char_length: int = Store._meta.get_field("state").max_length

        self.store: Store = StoreFactory()

    def test_name_within_100_chars(self):
        self.assertLessEqual(len(self.store.name), self.name_char_length, f"Store name field must be {self.name_char_length} characters or less.")

    def test_name_cant_exceed_100_chars(self):
        name: str = ''.join(random.choice(string.ascii_letters) for _ in range(self.name_char_length + 1))
        self.store.name = name

        with self.assertRaises(ValidationError):
            self.store.clean_fields()
            
        self.assertEqual(len(self.store.name), self.name_char_length + 1, f"Store name field must be {self.name_char_length} characters or less.")

    def test_user_delete_cascades_store(self):
        self.store.owner.delete()
        self.assertFalse(Store.objects.filter(pk=self.store.pk).exists())

    def test_store_doesnt_delete_cascade_user(self):
        self.store.delete()
        self.assertTrue(User.objects.filter(pk=self.store.owner.pk).exists())

    def test_city_within_25_chars(self):
        self.assertLessEqual(len(self.store.city), self.city_char_length, f"Store name field must be {self.city_char_length} characters or less.")

    def test_city_cant_exceed_25_chars(self):
        city: str = ''.join(random.choice(string.ascii_letters) for _ in range(self.city_char_length + 1))
        self.store.city = city

        with self.assertRaises(ValidationError):
            self.store.clean_fields()
            
        self.assertEqual(len(self.store.city), self.city_char_length + 1, f"Store name field must be {self.city_char_length} characters or less.")

    def test_state_within_25_chars(self):
        self.assertLessEqual(len(self.store.state), self.state_char_length, f"Store name field must be {self.state_char_length} characters or less.")

    def test_state_cant_exceed_25_chars(self):
        state: str = ''.join(random.choice(string.ascii_letters) for _ in range(self.state_char_length + 1))
        self.store.state = state

        with self.assertRaises(ValidationError):
            self.store.clean_fields()
            
        self.assertEqual(len(self.store.state), self.state_char_length + 1, f"Store name field must be {self.state_char_length} characters or less.")