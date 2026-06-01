import os
import django
import random
from datetime import time, date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from leave.models import LeaveRequest, LeaveType
from attendance.models import Attendance
from employees.models import Department, Employee

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

print("Cleaning up leave reasons...")
for req in LeaveRequest.objects.all():
    if any(bad in req.reason.lower() for bad in bad_reasons):
        req.reason = random.choice(good_reasons)
        req.save()

# 2. Delete unwanted users and their records
unwanted_names = ['donald', 'trump', 'shadow', 'brow']
print("Removing unwanted users...")
for u in User.objects.all():
    if any(unwanted in u.username.lower() or unwanted in u.first_name.lower() or unwanted in u.last_name.lower() for unwanted in unwanted_names):
        u.delete()

# 3. Add 6 new users with Sinhala names
sinhala_names = [
    ("Kasun", "Perera"),
    ("Nuwan", "Silva"),
    ("Chamara", "Fernando"),
    ("Oshadi", "Bandara"),
    ("Kavindi", "Rajapaksha"),
    ("Hasini", "Weerasinghe")
]

dept, _ = Department.objects.get_or_create(name='Operations')
leave_type = LeaveType.objects.first()

print("Adding new employees and generating records...")
for first, last in sinhala_names:
    username = f"{first.lower()}_{last.lower()}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f"{username}@example.com", 'password123', role='EMPLOYEE', first_name=first, last_name=last)
        Employee.objects.create(user=user, department=dept, designation='Executive', joining_date=date.today() - timedelta(days=random.randint(100, 1000)))
        
        # Add leaves
        for _ in range(random.randint(1, 3)):
            d1 = date(2026, random.randint(3, 6), random.randint(1, 28))
            d2 = d1 + timedelta(days=random.randint(1, 3))
            if leave_type:
                LeaveRequest.objects.create(
                    employee=user,
                    leave_type=leave_type,
                    start_date=d1,
                    end_date=d2,
                    reason=random.choice(good_reasons),
                    status=random.choice(['APPROVED', 'PENDING', 'REJECTED'])
                )
        
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

print("Data cleanup and generation successful!")
