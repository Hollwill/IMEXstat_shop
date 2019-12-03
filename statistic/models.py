from django.db import models


class StatisticData(models.Model):
    napr = models.CharField(max_length=2, db_index=True, blank=True, null=True)
    period = models.DateField(db_index=True, blank=True, null=True)
    strana = models.CharField(db_index=True, max_length=3, blank=True, null=True)
    tnved = models.CharField(db_index=True, max_length=10, blank=True, null=True)
    edizm = models.CharField(max_length=20, blank=True, null=True)
    stoim = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    netto = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    kol = models.DecimalField(max_digits=22, decimal_places=0, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    region_s = models.CharField(max_length=255, blank=True, null=True)
