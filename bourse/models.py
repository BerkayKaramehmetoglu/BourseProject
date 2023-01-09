from django.db import models
from djongo.models import ObjectIdField, ExpressionList

# Create your models here.

class Coin(models.Model):
    _id = ObjectIdField()
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50, unique=False)
    prices = models.JSONField()
    rank = models.IntegerField(default=0, blank=True)
    image = models.URLField(blank=True, null=True)
    momentary_up = models.FloatField(default=0, blank=True)
    momentary_down = models.FloatField(default=0, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['rank']
