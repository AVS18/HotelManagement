from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class Rooms(models.Model):
    room_name = models.CharField(max_length=50)
    room_desc = models.CharField(max_length=200)
    room_occ = models.IntegerField()
    room_price = models.IntegerField()
    no_of_rooms_avail = models.IntegerField()
    select =(('Economy','Economy'),('Premium','Premium'))
    room_class = models.CharField(max_length=10,choices=select) 
    room_img = models.ImageField(upload_to = 'room_pics/')
class User(AbstractUser):
    mobile = models.BigIntegerField(null=True)

class Contactus(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    message = models.CharField(max_length=500)