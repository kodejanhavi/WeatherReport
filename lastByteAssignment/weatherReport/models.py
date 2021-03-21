from django.db import models

# Create your models here.
class City(models.Model):
    cityid = models.BigAutoField(auto_created=True, primary_key=True, blank=False)
    cityname = models.CharField(max_length=25, unique=True)
    latitude = models.FloatField(blank= False , null=False)
    longitude = models.FloatField(blank= False , null=False)
    country = models.CharField(max_length=25)

class Admin(models.Model):
    adminid = models.BigAutoField(auto_created=True, primary_key=True, blank=False)
    username = models.CharField(max_length=10, unique=True, blank=False, null=False)
    password = models.CharField(max_length=10, blank=False, null=False)