from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Payroll
from .forms import PayrollForm

@login_required
def payroll_list(request):
    year_filter = request.GET.get('year', '')
    
    if request.user.role == 'HR':
        payrolls = Payroll.objects.select_related('employee').all()
    else:
        payrolls = Payroll.objects.filter(employee=request.user)
        
    if year_filter:
        payrolls = payrolls.filter(year=year_filter)
        
    paginator = Paginator(payrolls, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get distinct years for filter
    years = Payroll.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    context = {
        'payrolls': page_obj,
        'year_filter': year_filter,
        'years': years,
    }
    return render(request, 'payroll/list.html', context)

@login_required
def payroll_add(request):
    if request.user.role != 'HR': return redirect('dashboard')

    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Payroll record added successfully.')
                return redirect('payroll_list')
            except Exception as e:
                messages.error(request, 'A payroll record for this employee, month, and year already exists.')
    else:
        import datetime
        current_year = datetime.date.today().year
        current_month = str(datetime.date.today().month)
        form = PayrollForm(initial={'year': current_year, 'month': current_month})

    # Build a map of {user_id: base_salary} for auto-fill
    from employees.models import Employee as EmpModel
    import json
    salary_map = {str(e.user_id): str(e.base_salary) for e in EmpModel.objects.all()}

    return render(request, 'payroll/form.html', {
        'form': form,
        'title': 'Add Salary Record',
        'salary_map': json.dumps(salary_map),
    })

@login_required
def payroll_edit(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll record updated.')
            return redirect('payroll_list')
    else:
        form = PayrollForm(instance=payroll)

    # Build a map of {user_id: base_salary} for auto-fill
    from employees.models import Employee as EmpModel
    import json
    salary_map = {str(e.user_id): str(e.base_salary) for e in EmpModel.objects.all()}
        
    return render(request, 'payroll/form.html', {
        'form': form, 
        'title': 'Edit Salary Record',
        'salary_map': json.dumps(salary_map),
    })

@login_required
def payroll_delete(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        payroll.delete()
        messages.success(request, 'Payroll record deleted.')
        return redirect('payroll_list')
    return render(request, 'payroll/confirm_delete.html', {'payroll': payroll})

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def export_payroll_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Payroll Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    data = [['Employee', 'Period', 'Basic', 'Bonus', 'Deductions', 'Net Salary']]
    
    if request.user.role == 'HR':
        payrolls = Payroll.objects.select_related('employee').all().order_by('-year', '-month')
    else:
        payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
        
    for p in payrolls:
        data.append([
            p.employee.get_full_name() or p.employee.username,
            f"{p.get_month_display()} {p.year}",
            f"Rs. {p.basic_salary}",
            f"Rs. {p.bonus}",
            f"Rs. {p.deductions}",
            f"Rs. {p.net_salary}"
        ])
        
    t = Table(data, colWidths=[120, 80, 70, 70, 80, 80])
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
    return FileResponse(buffer, as_attachment=True, filename='payroll_report.pdf')
