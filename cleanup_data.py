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

# 1. Clean up inappropriate leave reasons and dates
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

    days_before = random.randint(2, 10)
    applied_date_naive = datetime.combine(req.start_date - timedelta(days=days_before), time(random.randint(8, 16), random.randint(0, 59)))
    applied_date_aware = timezone.make_aware(applied_date_naive)
    LeaveRequest.objects.filter(id=req.id).update(applied_on=applied_date_aware)

# 2. Delete unwanted users
unwanted_names = ['donald', 'trump', 'shadow', 'brow']
for u in User.objects.all():
    if any(unwanted in u.username.lower() or unwanted in u.first_name.lower() or unwanted in u.last_name.lower() for unwanted in unwanted_names):
        u.delete()

# 3. Diverse departments
departments = []
for d_name in ['IT', 'Finance', 'Marketing', 'Sales', 'Operations', 'Engineering']:
    dept, _ = Department.objects.get_or_create(name=d_name)
    departments.append(dept)

print("Randomizing departments for all employees...")
# FORCE update existing employees to have random departments
for emp in Employee.objects.all():
    emp.department = random.choice(departments)
    emp.save()

# 4. Add 6 new users with Sinhala names (if they don't exist yet)
sinhala_names = [
    ("Kasun", "Perera"),
    ("Nuwan", "Silva"),
    ("Chamara", "Fernando"),
    ("Oshadi", "Bandara"),
    ("Kavindi", "Rajapaksha"),
    ("Hasini", "Weerasinghe")
]

leave_type = LeaveType.objects.first()

for first, last in sinhala_names:
    username = f"{first.lower()}_{last.lower()}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f"{username}@example.com", 'password123', role='EMPLOYEE', first_name=first, last_name=last)
        
        emp_dept = random.choice(departments)
        Employee.objects.create(user=user, department=emp_dept, designation='Executive', joining_date=date.today() - timedelta(days=random.randint(100, 1000)))
        
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
                days_before = random.randint(2, 10)
                applied_date_naive = datetime.combine(d1 - timedelta(days=days_before), time(random.randint(8, 16), random.randint(0, 59)))
                applied_date_aware = timezone.make_aware(applied_date_naive)
                LeaveRequest.objects.filter(id=req.id).update(applied_on=applied_date_aware)
        
        for i in range(1, 6):
            d = date(2026, 4, i)
            if random.choice([True, False, True]):
                Attendance.objects.create(
                    employee=user,
                    date=d,
                    clock_in=time(8, random.randint(10, 50)),
                    clock_out=time(17, random.randint(0, 30)),
                    status='PRESENT',
                    is_late=False
                )

# 5. Populate the 'employee' test account with rich data
print("Populating test 'employee' account with data...")
test_user = User.objects.filter(username='employee').first()
if not test_user:
    test_user = User.objects.create_user('employee', 'employee@example.com', 'employee123', role='EMPLOYEE', first_name='John', last_name='Doe')
    dept = Department.objects.first()
    Employee.objects.create(user=test_user, department=dept, designation='Software Engineer', joining_date=date(2022, 1, 15))

LeaveRequest.objects.filter(employee=test_user).delete()
Attendance.objects.filter(employee=test_user).delete()

for i in range(4):
    d1 = date(2026, 3 + i, random.randint(1, 20))
    d2 = d1 + timedelta(days=random.randint(1, 3))
    if leave_type:
        req = LeaveRequest.objects.create(
            employee=test_user,
            leave_type=leave_type,
            start_date=d1,
            end_date=d2,
            reason=random.choice(good_reasons),
            status=random.choice(['APPROVED', 'PENDING', 'APPROVED', 'REJECTED'])
        )
        days_before = random.randint(2, 10)
        applied_date_naive = datetime.combine(d1 - timedelta(days=days_before), time(random.randint(8, 16), random.randint(0, 59)))
        applied_date_aware = timezone.make_aware(applied_date_naive)
        LeaveRequest.objects.filter(id=req.id).update(applied_on=applied_date_aware)

for i in range(1, 25):
    d = date(2026, 5, i)
    if d.weekday() < 5:  # Skip weekends
        if random.choice([True, True, True, False]): 
            Attendance.objects.create(
                employee=test_user,
                date=d,
                clock_in=time(8, random.randint(10, 50)),
                clock_out=time(17, random.randint(0, 45)),
                status='PRESENT',
                is_late=False
            )

print("Data cleanup and generation successful! Everything feels real now.")
