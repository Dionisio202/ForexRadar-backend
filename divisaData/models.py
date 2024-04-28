
from django.db import models

class ForexData(models.Model):
    FREQUENCY_CHOICES = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ]

    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default='D')

    class Meta:
        unique_together = ('symbol', 'date','frequency')
