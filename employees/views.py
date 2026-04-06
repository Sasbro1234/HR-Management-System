from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Employee, Department
from .forms import EmployeeForm

@login_required
def employee_list(request):
    if request.user.role != 'HR':
        return redirect('dashboard')
    
    query = request.GET.get('q', '')
    dept = request.GET.get('department', '')
    
    employees = Employee.objects.select_related('user', 'department').all().order_by('-id')
    
    if query:
        employees = employees.filter(user__first_name__icontains=query) | employees.filter(user__last_name__icontains=query)
    if dept:
        employees = employees.filter(department_id=dept)
        
    departments = Department.objects.all()
    
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employees': page_obj,
        'departments': departments,
        'query': query,
        'dept': dept,
    }
    return render(request, 'employees/list.html', context)

@login_required
def employee_create(request):
    if request.user.role != 'HR': return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Employee'})

@login_required
def employee_update(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee, user_instance=employee.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee, user_instance=employee.user)
        
    return render(request, 'employees/form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
def employee_delete(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.user.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def export_employees_pdf(request):
    if request.user.role != 'HR': return redirect('dashboard')
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Employee Directory", styles['Title']))
    elements.append(Spacer(1, 12))
    
    data = [['Name', 'Department', 'Designation', 'Joined Date']]
    for emp in Employee.objects.select_related('user', 'department').all().order_by('user__first_name'):
        data.append([
            emp.user.get_full_name() or emp.user.username,
            emp.department.name if emp.department else '-',
            emp.designation,
            emp.joining_date.strftime("%b %d, %Y") if emp.joining_date else '-'
        ])
        
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    doc.build(elements)
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='employees.pdf')
