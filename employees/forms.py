from django import forms
from django.contrib.auth import get_user_model
from .models import Employee, Department

User = get_user_model()

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Employee
        fields = ['department', 'designation', 'joining_date', 'phone_number', 'address', 'base_salary']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            self.fields['username'].initial = self.user_instance.username

        for field in self.fields.values():
            field.widget.attrs['class'] = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-3'
            
    def save(self, commit=True):
        employee = super().save(commit=False)
        if not self.user_instance:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='EMPLOYEE'
            )
            if self.cleaned_data.get('profile_picture'):
                user.profile_picture = self.cleaned_data['profile_picture']
                user.save()
            employee.user = user
        else:
            user = self.user_instance
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            if self.cleaned_data.get('profile_picture'):
                user.profile_picture = self.cleaned_data['profile_picture']
            user.save()
            
        if commit:
            employee.save()
        return employee
