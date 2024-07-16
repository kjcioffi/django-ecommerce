from django.db import models
from django.contrib.auth.models import User, AnonymousUser

class ProductManager(models.Manager):
    def filter_by_store(self, owner: User):
        """
        Fetches products associated with a store.
        """
        if owner != AnonymousUser:
            return self.filter(store__owner=owner)
        else:
            return self.none()