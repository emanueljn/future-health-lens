from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g. BRA
    name = models.CharField(max_length=200)

    def __str__(self): return f"{self.name} ({self.code})"

class Indicator(models.Model):
    code = models.CharField(max_length=64, unique=True)  # ex: WHOSIS_000001
    name = models.CharField(max_length=255)

    def __str__(self): return f"{self.name} - {self.code}"

class IndicatorValue(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='values')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='indicator_values')
    year = models.IntegerField()
    value = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('indicator', 'country', 'year')
        indexes = [
            models.Index(fields=['indicator', 'country', 'year'])
        ]

    def __str__(self):
        return f"{self.country.code} {self.indicator.code} {self.year}={self.value}"

