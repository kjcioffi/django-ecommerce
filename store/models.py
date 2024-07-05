from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Store(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    products = models.ManyToManyField(Product, through="OrderItem")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    street = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.total_cost = 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id}"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.order}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        order = self.order
        total_cost = sum(order_item.quantity * order_item.product.price for order_item in order.orderitem_set.all())
        order.total_cost = total_cost
        order.save()
        