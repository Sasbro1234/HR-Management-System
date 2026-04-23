from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Payroll(models.Model):
    MONTH_CHOICES = (
        ('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    )
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payrolls')
    month = models.CharField(max_length=2, choices=MONTH_CHOICES)
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    @property
    def net_salary(self):
        return self.basic_salary + self.bonus - self.deductions

    def clean(self):
        errors = {}

        if self.basic_salary <= 0:
            errors['basic_salary'] = "Basic salary must be greater than zero"

        if self.bonus < 0:
            errors['bonus'] = "Bonus cannot be negative"

        if self.deductions < 0:
            errors['deductions'] = "Deductions cannot be negative"

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.employee.username} - {self.get_month_display()} {self.year}"