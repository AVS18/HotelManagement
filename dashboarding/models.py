from django.db import models
from registration.models import User,Rooms
# Create your models here.
class RoomBooking(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()
    date_booked = models.DateField()
    is_cancelled = models.BooleanField()
    cancelled_date = models.DateField(null=True)
    total_days = models.IntegerField()
    cost = models.IntegerField()
    no_of_rooms = models.IntegerField(default=1)
    payment_ref = models.CharField(max_length=50)
    message = models.CharField(max_length=500,null=True)

class Availability(models.Model):
    room_type = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    date = models.DateField()
    month = models.CharField(max_length=20)
    rooms_available = models.IntegerField()

class Feedback(models.Model):
    room = models.ForeignKey(RoomBooking,on_delete = models.CASCADE)
    cleanliness = models.IntegerField()
    services = models.IntegerField()
    suggestions = models.CharField(max_length=200,null=True)