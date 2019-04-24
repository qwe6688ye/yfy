from django.db import models

# Create your models here.
class Movies(models.Model):
    name=models.CharField(max_length=30)
class Digital(models.Model):
    D_name=models.CharField(max_length=255)
    D_price=models.CharField(max_length=30)
    D_count=models.CharField(max_length=30)