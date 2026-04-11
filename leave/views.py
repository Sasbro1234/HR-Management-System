from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import LeaveRequest, LeaveType
from .forms import LeaveApplyForm

@login_required
def leave_list(request):
    status_filter = request.GET.get('status', '')
    
    if request.user.role == 'HR':
        leaves = LeaveRequest.objects.select_related('employee', 'leave_type').all().order_by('-applied_on')
    else:
        leaves = LeaveRequest.objects.filter(employee=request.user).select_related('leave_type').order_by('-applied_on')
        
    if status_filter:
        leaves = leaves.filter(status=status_filter)
        
    paginator = Paginator(leaves, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'leaves': page_obj,
        'status_filter': status_filter
    }
    return render(request, 'leave/list.html', context)

@login_required
def leave_apply(request):
    if request.user.role == 'HR':
        messages.warning(request, "HR Managers generally manage leaves rather than apply, but you can proceed.")
        
    if request.method == 'POST':
        form = LeaveApplyForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('leave_list')
    else:
        form = LeaveApplyForm()
        
    return render(request, 'leave/form.html', {'form': form})

@login_required
def leave_approve(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave.status = 'APPROVED'
        leave.reviewed_by = request.user
        leave.save()
        messages.success(request, f'Leave for {leave.employee.get_full_name()} approved.')
    return redirect('leave_list')

@login_required
def leave_reject(request, pk):
    if request.user.role != 'HR': return redirect('dashboard')
    
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave.status = 'REJECTED'
        leave.reviewed_by = request.user
        leave.save()
        messages.error(request, f'Leave for {leave.employee.get_full_name()} rejected.')
    return redirect('leave_list')
