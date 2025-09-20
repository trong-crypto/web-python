from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Facility, Booking, MaintenanceRecord
from .forms import FacilityForm, BookingForm

def index(request):
    return render(request, 'index.html')

def facility_list(request):
    facilities = Facility.objects.all()
    
    # Lọc theo trạng thái
    status_filter = request.GET.get('status')
    if status_filter:
        facilities = facilities.filter(status=status_filter)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        facilities = facilities.filter(
            Q(name__icontains=search_query) | 
            Q(serial_number__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    context = {
        'facilities': facilities,
        'status_choices': Facility.STATUS_CHOICES
    }
    return render(request, 'facility_list.html', context)

def facility_detail(request, id):
    facility = get_object_or_404(Facility, id=id)
    maintenance_records = MaintenanceRecord.objects.filter(facility=facility)
    bookings = Booking.objects.filter(facility=facility)
    
    context = {
        'facility': facility,
        'maintenance_records': maintenance_records,
        'bookings': bookings
    }
    return render(request, 'facility_detail.html', context)

@permission_required('facilities.add_facility')
def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thiết bị đã được thêm thành công!')
            return redirect('facility_list')
    else:
        form = FacilityForm()
    return render(request, 'facility_form.html', {'form': form, 'title': 'Thêm thiết bị mới'})

@permission_required('facilities.change_facility')
def facility_edit(request, id):
    facility = get_object_or_404(Facility, id=id)
    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thiết bị đã được cập nhật!')
            return redirect('facility_detail', id=id)
    else:
        form = FacilityForm(instance=facility)
    return render(request, 'facility_form.html', {'form': form, 'title': 'Chỉnh sửa thiết bị'})

@login_required
def booking_list(request):
    if request.user.has_perm('facilities.view_booking'):
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.filter(requester=request.user)
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_choices': Booking.STATUS_CHOICES
    }
    return render(request, 'booking_list.html', context)

@login_required
def booking_create(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.facility = facility
            booking.requester = request.user
            
            # Kiểm tra xem thiết bị có khả dụng không
            conflicting_bookings = Booking.objects.filter(
                facility=facility,
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time,
                status__in=['approved', 'pending']
            )
            
            if conflicting_bookings.exists():
                messages.error(request, 'Thiết bị không khả dụng trong khoảng thời gian này!')
            else:
                booking.save()
                messages.success(request, 'Yêu cầu đặt thiết bị đã được gửi!')
                return redirect('booking_list')
    else:
        form = BookingForm()
    
    return render(request, 'booking_form.html', {
        'form': form, 
        'facility': facility,
        'title': 'Đặt thiết bị'
    })

@permission_required('facilities.change_booking')
def booking_approve(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.status = 'approved'
    booking.save()
    messages.success(request, 'Đã phê duyệt yêu cầu đặt thiết bị!')
    return redirect('booking_list')

@permission_required('facilities.change_booking')
def booking_reject(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.status = 'rejected'
    booking.save()
    messages.success(request, 'Đã từ chối yêu cầu đặt thiết bị!')
    return redirect('booking_list')