from leave.models import LeaveRequest
from payroll.models import Payroll

def notifications(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.role == 'HR':
            pending = LeaveRequest.objects.filter(status='PENDING').order_by('-applied_on')[:5]
            context['pending_leaves'] = pending
            context['pending_leaves_count'] = pending.count()
        else:
            # Approved leaves (unseen — last 3)
            approved_leaves = LeaveRequest.objects.filter(
                employee=request.user, status='APPROVED'
            ).order_by('-applied_on')[:3]
            # Rejected leaves (unseen — last 3)
            rejected_leaves = LeaveRequest.objects.filter(
                employee=request.user, status='REJECTED'
            ).order_by('-applied_on')[:3]
            # Recent payrolls
            recent_payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')[:2]

            context['emp_approved_leaves'] = approved_leaves
            context['emp_rejected_leaves'] = rejected_leaves
            context['emp_recent_payrolls'] = recent_payrolls
            context['emp_notifications_count'] = approved_leaves.count() + rejected_leaves.count() + recent_payrolls.count()
    return context

