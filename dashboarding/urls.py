from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.dashboard, name="dashboard"),
    path('availrooms',views.availrooms,name="availrooms"),
    path('bookroom',views.bookroom,name="bookroom"),
    path('acceptBooking',views.acceptBooking,name="acceptBooking"),
    path('confirmBooking',views.confirmBooking,name="confirmBooking"),
    path('getVacancy',views.getVacancy,name="getVacancy"),
    path('pastBookings',views.pastBookings,name="pastBookings"),
    path('cancelBooking/<str:id>',views.cancelBooking,name="cancelBooking"),
    path('feedback',views.feedback,name="feedback")
]