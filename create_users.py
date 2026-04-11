import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='HR', first_name='HR', last_name='Manager')
    print("Created HR Manager: username='admin', password='admin123'")

if not User.objects.filter(username='employee').exists():
    user = User.objects.create_user('employee', 'employee@example.com', 'employee123', role='EMPLOYEE', first_name='John', last_name='Doe')
    from employees.models import Department, Employee
    import datetime
    dept, _ = Department.objects.get_or_create(name='Engineering')
    Employee.objects.create(user=user, department=dept, designation='Software Engineer', joining_date=datetime.date.today())
    print("Created Employee: username='employee', password='employee123'")
