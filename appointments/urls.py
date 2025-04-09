from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard URLs
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),

    # Appointment URLs
    path('appointment/create/', views.create_appointment, name='create_appointment'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/<int:pk>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
]