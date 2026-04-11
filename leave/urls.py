from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_list, name='leave_list'),
    path('apply/', views.leave_apply, name='leave_apply'),
    path('approve/<int:pk>/', views.leave_approve, name='leave_approve'),
    path('reject/<int:pk>/', views.leave_reject, name='leave_reject'),
]
