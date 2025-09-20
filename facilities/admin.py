from django.contrib import admin
from .models import FacilityCategory, Building, Room, Facility, MaintenanceRecord, Booking

@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'location')
    search_fields = ('name', 'code')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building', 'floor', 'capacity', 'room_type')
    list_filter = ('building', 'room_type')
    search_fields = ('room_number', 'building__name')

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'serial_number', 'status', 'room')
    list_filter = ('category', 'status', 'room__building')
    search_fields = ('name', 'serial_number')
    readonly_fields = ('purchase_date',)

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('facility', 'maintenance_date', 'next_maintenance', 'cost', 'technician')
    list_filter = ('maintenance_date',)
    search_fields = ('facility__name', 'technician')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('facility', 'requester', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('facility__name', 'requester__username')