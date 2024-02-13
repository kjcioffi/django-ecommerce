from decimal import Decimal
from store.models import Product


def create_products(quantity: int):
        products = []
        for i in range(quantity):
            product = Product.objects.create(
                name=f"Product {i}",
                rating=0,
                price=Decimal('10.99'),
                description="Test")
            products.append(product)
        return products