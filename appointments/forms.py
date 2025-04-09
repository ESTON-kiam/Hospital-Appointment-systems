from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Doctor, Patient, Appointment, Prescription

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    pincode = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone',
                  'address', 'city', 'state', 'country', 'pincode',
                  'password1', 'password2']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'specialization', 'experience',
                  'consultation_fee', 'bio', 'available_days',
                  'start_time', 'end_time']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['blood_group', 'allergies', 'medical_history']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicine', 'dosage', 'instructions']