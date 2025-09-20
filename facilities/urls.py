from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('facilities/', views.facility_list, name='facility_list'),
    path('facilities/<int:id>/', views.facility_detail, name='facility_detail'),
    path('facilities/create/', views.facility_create, name='facility_create'),
    path('facilities/<int:id>/edit/', views.facility_edit, name='facility_edit'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('facilities/<int:facility_id>/book/', views.booking_create, name='booking_create'),
    path('bookings/<int:id>/approve/', views.booking_approve, name='booking_approve'),
    path('bookings/<int:id>/reject/', views.booking_reject, name='booking_reject'),
]