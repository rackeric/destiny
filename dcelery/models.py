from django.db import models

# Create your models here.

class SampleCount(models.Model):
    num = models.IntegerField(default=0)
