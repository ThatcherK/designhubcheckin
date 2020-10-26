from django.db import models

# Create your models here.
class Visitors(models.Model):
    name = models.CharField(max_length=200)
    temperature = models.IntegerField()
    company = models.CharField(max_length=200)
    identification_number = models.CharField(max_length=200, blank=True)
    telephone_number = models.IntegerField()
    date = models.DateField('date recorded')

    def __str__(self):
        return self.name
