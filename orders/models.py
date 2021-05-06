from django.db import models

from django.contrib.auth.models import User

# Create your models here.

# Menu

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class RegularPizza(models.Model):
    num_of_toppings = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.num_of_toppings}: S: ${self.small_price} L: ${self.large_price}"


class SicilianPizza(models.Model):
    num_of_toppings = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.num_of_toppings}: S: ${self.small_price} L: ${self.large_price}"


class Sub(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    large_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    available_toppings = models.ManyToManyField(Topping, blank=True, related_name="availableToppings")

    def __str__(self):
        return f"{self.name} S: ${self.small_price} L: ${self.large_price}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}(${self.price})"


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}(${self.price})"


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}: S: ${self.small_price} L: ${self.large_price}"

# Orders

class Order(models.Model):
    STATUS_CHOICES = ( 
    ("Prepairing", "Prepairing"), 
    ("Cooking", "Cooking"), 
    ("Delivering", "Delivering"), 
    ("Done", "Done"),  
    ) 
    ID = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32)
    order = models.TextField()
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"#{self.ID} by {self.user} Total: ${self.total}"
    