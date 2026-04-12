from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('add/', views.payroll_add, name='payroll_add'),
    path('edit/<int:pk>/', views.payroll_edit, name='payroll_edit'),
    path('delete/<int:pk>/', views.payroll_delete, name='payroll_delete'),
    path('export/', views.export_payroll_pdf, name='export_payroll'),
]
