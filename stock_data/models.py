from django.db import models

class HistoricalData(models.Model):
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
