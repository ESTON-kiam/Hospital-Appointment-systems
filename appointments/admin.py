# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Department, Appointment, Prescription

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient')
    list_filter = ('is_doctor', 'is_patient')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'country', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor', 'is_patient', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialization', 'consultation_fee')
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'specialization')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group')
    search_fields = ('user__first_name', 'user__last_name')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('appointment__patient__user__first_name', 'appointment__patient__user__last_name')

# Register models - order matters for foreign key relationships
admin.site.register(User, CustomUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)

