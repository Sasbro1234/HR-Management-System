from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('punch-in/', views.punch_in, name='punch_in'),
    path('punch-out/', views.punch_out, name='punch_out'),
]
