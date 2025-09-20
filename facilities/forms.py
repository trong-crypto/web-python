from django import forms
from .models import Facility, Booking, MaintenanceRecord

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'category', 'model', 'serial_number', 
                 'purchase_date', 'status', 'room', 'notes', 'image']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Tên thiết bị',
            'category': 'Danh mục',
            'model': 'Model',
            'serial_number': 'Số serial',
            'purchase_date': 'Ngày mua',
            'status': 'Trạng thái',
            'room': 'Phòng',
            'notes': 'Ghi chú',
            'image': 'Hình ảnh',
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'purpose']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'start_time': 'Thời gian bắt đầu',
            'end_time': 'Thời gian kết thúc',
            'purpose': 'Mục đích sử dụng',
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_date', 'next_maintenance', 'cost', 'description', 'technician']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'maintenance_date': 'Ngày bảo trì',
            'next_maintenance': 'Ngày bảo trì tiếp theo',
            'cost': 'Chi phí (VND)',
            'description': 'Mô tả công việc',
            'technician': 'Kỹ thuật viên',
        }