from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=15)
    model = models.CharField(max_length=15)
    year = models.IntegerField()
    color = models.CharField(max_length=15)
    price = models.IntegerField()
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)

    def __str__(self):
        return f'{self.name} {self.model} {self.year} {self.color} {self.price}'
