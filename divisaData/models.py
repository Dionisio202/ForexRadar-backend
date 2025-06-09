
from django.db import models
from django.contrib.auth.models import User

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



class Divisa(models.Model):
    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10)
    imagen1 = models.URLField(max_length=500, default='https://example.com/imagen1.png')
    imagen2 = models.URLField(max_length=500, default='https://example.com/imagen2.png')


    def __str__(self):
        return f'{self.nombre} ({self.simbolo})'


class UserDivisa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    divisa = models.ForeignKey(Divisa, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'divisa')