from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from leave.models import LeaveRequest, LeaveType
from attendance.models import Attendance
from payroll.models import Payroll
from employees.models import Department
from django.db.models import Count, Sum
import datetime

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing_page.html')

@login_required
def dashboard(request):
    today = datetime.date.today()
    current_year = today.year

    if request.user.role == 'HR':
        total_employees = User.objects.filter(role='EMPLOYEE').count()
        present_today = Attendance.objects.filter(date=today, status='PRESENT').count()
        
        # Monthly payroll total (current month) - net_salary is a property, not a DB field
        payrolls_this_month = Payroll.objects.filter(month=str(today.month), year=current_year)
        total_monthly_payroll = sum(p.basic_salary + p.bonus - p.deductions for p in payrolls_this_month)
        
        # Department breakdown
        dept_data = Department.objects.annotate(emp_count=Count('employee'))
        dept_labels = [d.name for d in dept_data]
        dept_counts = [d.emp_count for d in dept_data]
        
        # -- Real Leave Trend Data: approved leaves by start_date month --
        leave_trend_data = []
        for m in range(1, 13):
            count = LeaveRequest.objects.filter(
                status='APPROVED',
                start_date__year=current_year,
                start_date__month=m
            ).count()
            leave_trend_data.append(count)

        # -- Monthly Payroll Bar Chart: net salary per month (computed in Python) --
        monthly_payroll_data = []
        for m in range(1, 13):
            rows = Payroll.objects.filter(month=str(m), year=current_year)
            total = sum(float(p.basic_salary + p.bonus - p.deductions) for p in rows)
            monthly_payroll_data.append(total)

        context = {
            'total_employees': total_employees,
            'present_today': present_today,
            'total_monthly_payroll': total_monthly_payroll,
            'dept_labels': dept_labels,
            'dept_counts': dept_counts,
            'leave_trend_data': leave_trend_data,
            'total_approved_leaves': sum(leave_trend_data),
            'monthly_payroll_data': monthly_payroll_data,
            'month_names': MONTH_NAMES,
            'current_year': current_year,
        }
        return render(request, 'dashboard/hr_dashboard.html', context)
    else:
        # EMPLOYEE Dashboard Logic
        total_allowed = sum(lt.days_allowed for lt in LeaveType.objects.all())
        used_leaves = sum(
            l.duration for l in LeaveRequest.objects.filter(
                employee=request.user, status='APPROVED', applied_on__year=today.year
            )
        )
        remaining_leaves = total_allowed - used_leaves

        attendance_today = Attendance.objects.filter(employee=request.user, date=today).first()
        recent_payslip = Payroll.objects.filter(employee=request.user).order_by('-year', '-month').first()

        context = {
            'remaining_leaves': remaining_leaves,
            'attendance_today': attendance_today,
            'recent_payslip': recent_payslip,
        }
        return render(request, 'dashboard/emp_dashboard.html', context)



