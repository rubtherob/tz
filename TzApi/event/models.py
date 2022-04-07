from django.db import models

# Create your models here.
class Event(models.Model):
    date = models.DateField()
    views = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    costs = models.DecimalField(max_digits=100, decimal_places=2)
