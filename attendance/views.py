from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import time
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Attendance

@login_required
def attendance_list(request):
    date_filter = request.GET.get('date', '')
    
    if request.user.role == 'HR':
        records = Attendance.objects.select_related('employee').all()
    else:
        records = Attendance.objects.filter(employee=request.user)
        
    if date_filter:
        records = records.filter(date=date_filter)
        
    paginator = Paginator(records, 15)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    
    today = timezone.localdate()
    today_attendance = Attendance.objects.filter(employee=request.user, date=today).first()
    
    context = {
        'records': page_obj,
        'date_filter': date_filter,
        'today_attendance': today_attendance,
        'today': today
    }
    return render(request, 'attendance/list.html', context)

@login_required
def punch_in(request):
    if request.method == 'POST' and request.user.role == 'EMPLOYEE':
        today = timezone.localdate()
        now = timezone.localtime().time()
        
        attendance, created = Attendance.objects.get_or_create(
            employee=request.user,
            date=today,
            defaults={'clock_in': now, 'status': 'PRESENT'}
        )
        if now > time(9, 0):   #checking if checked in after 9#
            attendance.is_late = True
        else:
            attendance.is_late = False

        attendance.save()
        
        if created:
            messages.success(request, f"Punched in successfully at {now.strftime('%I:%M %p')}")
        else:
            messages.info(request, "You have already punched in today.")
            
    return redirect('attendance_list')

@login_required
def punch_out(request):
    if request.method == 'POST' and request.user.role == 'EMPLOYEE':
        today = timezone.localdate()
        now = timezone.localtime().time()
        
        attendance = Attendance.objects.filter(employee=request.user, date=today).first()
        if attendance:
            if not attendance.clock_out:
                attendance.clock_out = now
                attendance.save()
                messages.success(request, f"Punched out successfully at {now.strftime('%I:%M %p')}")
            else:
                messages.info(request, "You have already punched out today.")
        else:
            messages.error(request, "You must punch in first.")
            
    return redirect('attendance_list')
