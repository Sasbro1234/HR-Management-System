import os
import django
import random
from datetime import time, date, timedelta, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from leave.models import LeaveRequest, LeaveType
from attendance.models import Attendance
from employees.models import Department, Employee
from django.utils import timezone

User = get_user_model()

# 1. Clean up inappropriate leave reasons
bad_reasons = ['game yanawa', 'war', 'diarrhea', 'shadow', 'brow']
good_reasons = [
    'Family Vacation',
    'Personal Leave',
    'Sick Leave',
    'Attending a family wedding',
    'Medical appointment',
    'Bank matters',
    'Childcare'
]

print("Cleaning up leave reasons and dates...")
for req in LeaveRequest.objects.all():
    changed = False
    if any(bad in req.reason.lower() for bad in bad_reasons):
        req.reason = random.choice(good_reasons)
        changed = True
    
    if changed:
        req.save()

    # Backdate the applied_on date so they don't all say "today"
    # Applied date should be 2-10 days BEFORE the start date
    days_before = random.randint(2, 10)
    applied_date_naive = datetime.combine(req.start_date - timedelta(days=days_before), time(random.randint(8, 16), random.randint(0, 59)))
    applied_date_aware = timezone.make_aware(applied_date_naive)
    LeaveRequest.objects.filter(id=req.id).update(applied_on=applied_date_aware)

# 2. Delete unwanted users and their records
unwanted_names = ['donald', 'trump', 'shadow', 'brow']
print("Removing unwanted users...")
for u in User.objects.all():
    if any(unwanted in u.username.lower() or unwanted in u.first_name.lower() or unwanted in u.last_name.lower() for unwanted in unwanted_names):
        u.delete()

# 3. Add 6 new users with Sinhala names and diverse departments
sinhala_names = [
    ("Kasun", "Perera"),
    ("Nuwan", "Silva"),
    ("Chamara", "Fernando"),
    ("Oshadi", "Bandara"),
    ("Kavindi", "Rajapaksha"),
    ("Hasini", "Weerasinghe")
]

# Create diverse departments
departments = []
for d_name in ['IT', 'Finance', 'Marketing', 'Sales', 'Operations', 'Engineering']:
    dept, _ = Department.objects.get_or_create(name=d_name)
    departments.append(dept)

leave_type = LeaveType.objects.first()

print("Adding new employees with diverse departments and generating realistic records...")
for first, last in sinhala_names:
    username = f"{first.lower()}_{last.lower()}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f"{username}@example.com", 'password123', role='EMPLOYEE', first_name=first, last_name=last)
        
        # Assign random department
        emp_dept = random.choice(departments)
        Employee.objects.create(user=user, department=emp_dept, designation='Executive', joining_date=date.today() - timedelta(days=random.randint(100, 1000)))
        
        # Add leaves
        for _ in range(random.randint(1, 3)):
            d1 = date(2026, random.randint(3, 6), random.randint(1, 28))
            d2 = d1 + timedelta(days=random.randint(1, 3))
            if leave_type:
                req = LeaveRequest.objects.create(
                    employee=user,
                    leave_type=leave_type,
                    start_date=d1,
                    end_date=d2,
                    reason=random.choice(good_reasons),
                    status=random.choice(['APPROVED', 'PENDING', 'REJECTED'])
                )
                # Overwrite applied_on to be realistic (before the leave starts)
                days_before = random.randint(2, 10)
                applied_date_naive = datetime.combine(d1 - timedelta(days=days_before), time(random.randint(8, 16), random.randint(0, 59)))
                applied_date_aware = timezone.make_aware(applied_date_naive)
                LeaveRequest.objects.filter(id=req.id).update(applied_on=applied_date_aware)
        
        # Add attendance
        for i in range(1, 6):
            d = date(2026, 4, i)
            if random.choice([True, False, True]): # 66% present chance
                Attendance.objects.create(
                    employee=user,
                    date=d,
                    clock_in=time(8, random.randint(10, 50)),
                    clock_out=time(17, random.randint(0, 30)),
                    status='PRESENT',
                    is_late=False
                )

print("Data cleanup and generation successful! Everything feels real now.")
