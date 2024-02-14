from decimal import Decimal

from django.test import override_settings
from store.models import Product

from django.core.files.uploadedfile import SimpleUploadedFile


@override_settings(MEDIA_ROOT=('media/tests'))
def create_products(quantity: int):
        products = []
        image_path = "media/products/test_file.png"
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        for i in range(quantity):
            product = Product.objects.create(
                name=f"Product {i}",
                rating=0,
                price=Decimal('10.99'),
                description="Test",
                image=image)
            products.append(product)
        return products