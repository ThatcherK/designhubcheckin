from django.db import models
from django.utils import timezone

# Create your models here.
class Visitors(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    identification_number = models.CharField(max_length=200, blank=True)
    telephone_number = models.CharField(max_length=100)
    date = models.DateTimeField( default=timezone.now)
      

    def __str__(self):
        return self.name

class Register(models.Model):
    visitor = models.ForeignKey(Visitors,on_delete=models.CASCADE)
    temperature = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    