from django.db import models
from django.conf import settings
# Create your models here.
class Movie(models.Model):
  hall = models.CharField(max_length=10)
  movie = models.CharField(max_length=10)
  date = models.DateField()

  def __str__(self):
    return self.movie

class Guest(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=30)
  phone = models.CharField(max_length=15)
  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

class Reservation(models.Model):
  guest = models.ForeignKey(Guest, on_delete=models.CASCADE , related_name='reservation')
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE , related_name='reservation')