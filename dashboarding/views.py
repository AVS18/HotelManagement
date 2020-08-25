from django.shortcuts import render, redirect
from django.contrib import auth, messages
import random
from django.core.mail import send_mail
from registration.models import Rooms,User
import datetime
from .models import RoomBooking, Availability, Feedback

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
def availrooms(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    eco = Rooms.objects.filter(room_class="Economy").all()
    pre = Rooms.objects.filter(room_class="Premium").all()
    return render(request,'avail_room.html',{'eco':eco,'pre':pre})


def bookroom(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')    
    obj = Rooms.objects.values('room_name')
    return render(request,'book_a_room.html',{'room_select':False,'obj':obj})

def acceptBooking(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        obj = Rooms.objects.filter(room_name=request.POST["room"]).all()[0]
        return render(request,'book_a_room.html',{'room_select':True,'obj':obj})
    else:
        return redirect('/dashboard/bookroom') 

def confirmBooking(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        user = User.objects.filter(username=request.user.username)[0]
        room = Rooms.objects.filter(room_name = request.POST["book_room_type"])[0]
        check_in_date = request.POST["check_in_date"]
        check_in_time = request.POST["check_in_time"]
        check_out_date = request.POST["check_out_date"]
        check_out_time = request.POST["check_out_time"]
        date_booked = datetime.datetime.today().strftime("%Y-%m-%d")
        is_cancelled = False
        total_days = request.POST["days"]
        cost = request.POST["amount"]
        payment_ref = request.POST["payment_id"]
        message = request.POST["message_desk"]
        no_of_rooms = request.POST["rooms_count"]
        #check whether requested rooms available on the days
        start_date = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        flag = True #We Initially assume rooms are available to book. We prove our assumption by checking the availability table
        while start_date<=end_date:
            val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=room)
            if len(val)!=0:
                if val[0].rooms_available < int(no_of_rooms):
                    flag=False 
                    break
            start_date += delta
        if not flag:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are not available between {2} - {3} Kindly Check the Vacancy again'.format(no_of_rooms,room.room_name,check_in_date,check_out_date))
            return redirect('/dashboard')
        obj = RoomBooking.objects.create(user=user,room=room,check_in_date=check_in_date,check_in_time=check_in_time,no_of_rooms=no_of_rooms,
                    check_out_date=check_out_date,check_out_time=check_out_time,date_booked=date_booked,is_cancelled=is_cancelled,
                    total_days=total_days,cost = cost,payment_ref=payment_ref,message = message)
        start_date = datetime.datetime.strptime(obj.check_in_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(obj.check_out_date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        while start_date<=end_date:
            val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=obj.room)
            if len(val)==0:
                Availability.objects.create(room_type=obj.room,date=start_date,month=start_date.month,rooms_available=int(obj.room.no_of_rooms_avail)-int(obj.no_of_rooms))
            else:
                avail = Availability.objects.get(date=start_date,month=start_date.month,room_type=obj.room)
                avail.rooms_available=int(avail.rooms_available)-int(obj.no_of_rooms)
                avail.save()
            start_date += delta
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'You have successfully booked rooms. We mailed you the further details of booking. We are waiting for your arrival.')
        msg = 'Dear '+request.user.first_name+',\n\n We have booked the Room with Booking Id BK'+str(obj.id)+' Successfully. Kindly visit your dashboard for more details.\n\nThank you.\nNova Luxury Hotel'
        send_mail('Room Booked Successfully',msg,from_email='adityaintern11@gmail.com',recipient_list=[request.user.email])
        return redirect('/dashboard')
    
def getVacancy(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        vacant_date = request.POST["vacant_date"]
        room = request.POST["room"]
        val = Availability.objects.filter(date=vacant_date,room_type__room_name=room)
        if len(val)==0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are available on {2}'.format(Rooms.objects.filter(room_name=room)[0].no_of_rooms_avail,room,vacant_date))
            return redirect('/dashboard')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are available on {2}'.format(val[0].rooms_available,room,vacant_date))
            return redirect('/dashboard')
    obj = Rooms.objects.all()
    return render(request,'vacancy.html',{'obj':obj})

def pastBookings(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    obj = RoomBooking.objects.filter(user__username=request.user.username,is_cancelled=False).select_related()
    li_up, li_past = [] , []
    today_date = datetime.date.today()
    for item in obj:
        if item.check_in_date>today_date:
            li_up.append(item)
        else:
            li_past.append(item)
    obj2 = RoomBooking.objects.filter(user__username=request.user.username,is_cancelled=True).select_related()
    len_li_up = len(li_up)
    len_li_past = len(li_past)
    len_obj2 = len(obj2)
    return render(request,'pastBookings.html',{'li_up':li_up,'li_past':li_past,'canc':obj2,'len_li_up':len_li_up,'len_li_past':len_li_past,'len_obj2':len_obj2})

def cancelBooking(request,id):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    obj = RoomBooking.objects.get(id=id)
    obj.is_cancelled=True
    obj.cancelled_date=datetime.date.today()
    obj.save()
    start_date = obj.check_in_date
    end_date = obj.check_out_date
    delta = datetime.timedelta(days=1)
    while start_date<=end_date:
        val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=obj.room)
        avail = Availability.objects.get(date=start_date,month=start_date.month,room_type=obj.room)
        avail.rooms_available=int(avail.rooms_available)+int(obj.no_of_rooms)
        avail.save()
        start_date += delta
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'You have successfully Cancelled Rooms of Booking Id BK:'+str(id))
    msg = 'Dear '+request.user.first_name+',\n\n We have cancelled the Room with Booking Id BK'+str(id)+' Successfully. Kindly visit your dashboard for more details.\n\nThank you.\nNova Luxury Hotel'
    send_mail('Room Booking Cancelled Successfully',msg,from_email='adityaintern11@gmail.com',recipient_list=[request.user.email])
    return redirect('/dashboard')

def feedback(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        room = request.POST["book_id"]
        cleanliness = request.POST["rate_clean"]
        services = request.POST["rate_service"]
        message = request.POST["rate_message"]
        Feedback.objects.create(room=RoomBooking.objects.filter(id=room)[0],cleanliness=cleanliness,services=services,suggestions=message)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Thank you for the feedback '+request.user.first_name)
        return redirect('/dashboard')
    obj = RoomBooking.objects.filter(user__username=request.user.username)
    li_up = []
    today_date = datetime.date.today()
    for item in obj:
        if item.check_in_date<=today_date and len(Feedback.objects.filter(room__id=item.id))==0:
            li_up.append(item)
    if len(li_up)==0:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'You have already Provided Feedback for the Past Bookings. Thank you for your cooperation.')
        return redirect('/dashboard')
    return render(request,'feedback.html',{'li_up':li_up})