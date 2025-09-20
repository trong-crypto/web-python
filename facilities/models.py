from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class FacilityCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Danh mục cơ sở vật chất"
        verbose_name_plural = "Danh mục cơ sở vật chất"

class Building(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên tòa nhà")
    code = models.CharField(max_length=10, unique=True, verbose_name="Mã tòa nhà")
    location = models.CharField(max_length=200, verbose_name="Vị trí")
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = "Tòa nhà"
        verbose_name_plural = "Tòa nhà"

class Room(models.Model):
    room_number = models.CharField(max_length=10, verbose_name="Số phòng")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Tòa nhà")
    floor = models.IntegerField(verbose_name="Tầng")
    capacity = models.IntegerField(verbose_name="Sức chứa")
    room_type = models.CharField(max_length=50, verbose_name="Loại phòng", 
                                choices=[('classroom', 'Phòng học'), ('lab', 'Phòng thí nghiệm'), 
                                         ('office', 'Văn phòng'), ('other', 'Khác')])
    
    def __str__(self):
        return f"{self.building.code}-{self.room_number}"
    
    class Meta:
        verbose_name = "Phòng"
        verbose_name_plural = "Phòng"
        unique_together = ('room_number', 'building')

class Facility(models.Model):
    STATUS_CHOICES = [
        ('available', 'Sẵn sàng'),
        ('in_use', 'Đang sử dụng'),
        ('maintenance', 'Bảo trì'),
        ('broken', 'Hư hỏng'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Tên thiết bị")
    category = models.ForeignKey(FacilityCategory, on_delete=models.CASCADE, verbose_name="Danh mục")
    model = models.CharField(max_length=100, blank=True, verbose_name="Model")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Số serial")
    purchase_date = models.DateField(verbose_name="Ngày mua")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Trạng thái")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vị trí")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    image = models.ImageField(upload_to='facilities/', blank=True, null=True, verbose_name="Hình ảnh")
    
    def __str__(self):
        return f"{self.name} - {self.serial_number}"
    
    class Meta:
        verbose_name = "Cơ sở vật chất"
        verbose_name_plural = "Cơ sở vật chất"

class MaintenanceRecord(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name="Thiết bị")
    maintenance_date = models.DateField(verbose_name="Ngày bảo trì")
    next_maintenance = models.DateField(verbose_name="Ngày bảo trì tiếp theo")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Chi phí")
    description = models.TextField(verbose_name="Mô tả công việc")
    technician = models.CharField(max_length=100, verbose_name="Kỹ thuật viên")
    
    def __str__(self):
        return f"Bảo trì {self.facility.name} - {self.maintenance_date}"
    
    class Meta:
        verbose_name = "Lịch sử bảo trì"
        verbose_name_plural = "Lịch sử bảo trì"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('completed', 'Hoàn thành'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, verbose_name="Thiết bị")
    requester = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người yêu cầu")
    start_time = models.DateTimeField(verbose_name="Thời gian bắt đầu")
    end_time = models.DateTimeField(verbose_name="Thời gian kết thúc")
    purpose = models.TextField(verbose_name="Mục đích sử dụng")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    def __str__(self):
        return f"{self.facility.name} - {self.requester.username}"
    
    class Meta:
        verbose_name = "Đặt thiết bị"
        verbose_name_plural = "Đặt thiết bị"