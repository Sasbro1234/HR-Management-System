from django import forms
from .models import Payroll

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'month', 'year', 'basic_salary', 'bonus', 'deductions']
        widgets = {
            'employee': forms.Select(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
            'month': forms.Select(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
            'year': forms.NumberInput(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3', 'step': '0.01'}),
            'bonus': forms.NumberInput(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3', 'step': '0.01'}),
            'deductions': forms.NumberInput(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3', 'step': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        # Only show employees in the dropdown
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['employee'].queryset = User.objects.filter(role='EMPLOYEE')
