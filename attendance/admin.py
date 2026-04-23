from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'is_late')

admin.site.register(Attendance, AttendanceAdmin)
