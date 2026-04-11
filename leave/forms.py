from django import forms
from .models import LeaveRequest

class LeaveApplyForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
            'reason': forms.Textarea(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3', 'rows': 4}),
            'leave_type': forms.Select(attrs={'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none mb-3'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        
        if start and end and start > end:
            raise forms.ValidationError("End date cannot be before start date.")
        return cleaned_data
