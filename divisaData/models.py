
from django.db import models

class ForexData(models.Model):
    symbol = models.CharField(max_length=10)  # Ejemplo: 'EURUSD'
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    class Meta:
        unique_together = ('symbol', 'date')
