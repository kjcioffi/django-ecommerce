from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    products = models.ManyToManyField(Product)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')])
    street = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)

    def __str__(self):
        return f"Order for {self.first_name} {self.last_name}"
