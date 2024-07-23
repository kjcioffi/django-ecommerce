from django.db import models
from django.contrib.auth.models import User


class StoreManager(models.Manager):
    def for_user_admin(self, owner: User):
        """
        Fetches the first store a user owns.
        """
        return self.filter(owner=owner).first()


class ProductManager(models.Manager):
    def filter_by_store(self, store):
        """
        Fetches products associated with a store.
        """
        return self.filter(store=store)


class OrderManager(models.Manager):
    def filter_by_store(self, store):
        """
        Fetches products associated with a store.
        """
        return self.filter(store=store)
