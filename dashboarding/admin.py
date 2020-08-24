from django.contrib import admin
from .models import RoomBooking,Availability,Feedback
# Register your models here.
class RoomBookingRef(admin.ModelAdmin):
    list_display = ['user','room','total_days','cost','no_of_rooms','payment_ref']
    list_filter = ['check_in_date','check_out_date','check_in_time','check_out_time','is_cancelled']
admin.site.register(RoomBooking,RoomBookingRef)
class AvailabilityRef(admin.ModelAdmin):
    list_filter = ['room_type','month','date']
    list_display = ['room_type','month','date','rooms_available']
admin.site.register(Availability,AvailabilityRef)
class FeedbackRef(admin.ModelAdmin):
    list_display = ['room','cleanliness','services','suggestions']
admin.site.register(Feedback,FeedbackRef)