from django.contrib import admin
from .models import User, Rooms, Contactus
# Register your models here.
class RoomRef(admin.ModelAdmin):
    list_display = ['room_name','room_occ','room_price','no_of_rooms_avail']
    list_filter = ['room_class']

class UserRef(admin.ModelAdmin):
    list_display = ['first_name','email','mobile','last_login']

class Contact(admin.ModelAdmin):
    list_display = ['name','email','mobile','message']

admin.site.register(Rooms,RoomRef)
admin.site.register(User,UserRef)
admin.site.register(Contactus,Contact)
