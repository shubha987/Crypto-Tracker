from django.db import models

class HistoricalData(models.Model):
    token = models.CharField(max_length=255)
    date = models.DateField()
    balance = models.DecimalField(max_digits=20, decimal_places=8)
