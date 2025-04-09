from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from .models import User, Doctor, Patient, Appointment, Prescription, Department
from .forms import (UserRegisterForm, DoctorProfileForm, PatientProfileForm,
                    AppointmentForm, PrescriptionForm)


# Utility functions
def is_doctor(user):
    return user.is_authenticated and user.is_doctor


def is_patient(user):
    return user.is_authenticated and user.is_patient


# Auth Views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = request.POST.get('user_type', 'patient')

            # Set user type
            user.is_doctor = (user_type == 'doctor')
            user.is_patient = (user_type == 'patient')

            # Save with proper password hashing
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create profile
            if user.is_doctor:
                # Add default values for required fields
                default_time = timezone.now().time()
                Doctor.objects.create(
                    user=user,
                    specialization="General",
                    experience="0 years",
                    consultation_fee=0.00,
                    available_days="Monday-Friday",
                    start_time=default_time,
                    end_time=default_time
                )
            else:
                Patient.objects.create(user=user)

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'appointments/register.html', {'form': form})


def auth_login(request, user):
    pass


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Handle 'next' redirect
            next_url = request.POST.get('next', '')
            if next_url:
                return redirect(next_url)
            # Redirect based on user type
            if user.is_doctor:
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    # Get the 'next' parameter from GET request
    next_url = request.GET.get('next', '')
    return render(request, 'appointments/login.html', {'next': next_url})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Dashboard Views
@login_required
@user_passes_test(is_doctor, login_url='login')
def doctor_dashboard(request):
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')
    today_appointments = appointments.filter(date=timezone.now().date(), status='confirmed')

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'today_appointments': today_appointments,
    }
    return render(request, 'appointments/doctor_dashboard.html', context)


@login_required
@user_passes_test(is_patient, login_url='login')
def patient_dashboard(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')

    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'appointments/patient_dashboard.html', context)


# Profile Views
@login_required
def profile(request):
    user = request.user
    if user.is_doctor:
        return redirect('doctor_profile')
    else:
        return redirect('patient_profile')


@login_required
@user_passes_test(is_doctor, login_url='login')
def doctor_profile(request):
    doctor = request.user.doctor
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'appointments/profile.html', {'form': form, 'user_type': 'doctor'})


@login_required
@user_passes_test(is_patient, login_url='login')
def patient_profile(request):
    patient = request.user.patient
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patient_profile')
    else:
        form = PatientProfileForm(instance=patient)

    return render(request, 'appointments/profile.html', {'form': form, 'user_type': 'patient'})


# Appointment Views
@login_required
@user_passes_test(is_patient, login_url='login')
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Appointment created successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {'form': form})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    # Check if the user has permission to view this appointment
    if not (request.user == appointment.doctor.user or request.user == appointment.patient.user):
        messages.error(request, 'You are not authorized to view this appointment.')
        return redirect('login')

    if request.method == 'POST' and request.user.is_doctor:
        prescription_form = PrescriptionForm(request.POST)
        if prescription_form.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            messages.success(request, 'Prescription added successfully!')
            return redirect('appointment_detail', pk=pk)
    else:
        prescription_form = PrescriptionForm()

    prescriptions = Prescription.objects.filter(appointment=appointment)

    context = {
        'appointment': appointment,
        'prescription_form': prescription_form,
        'prescriptions': prescriptions,
    }
    return render(request, 'appointments/appointment_detail.html', context)


@login_required
@user_passes_test(is_doctor, login_url='login')
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)

    if appointment.doctor.user != request.user:
        messages.error(request, 'You are not authorized to update this appointment.')
        return redirect('doctor_dashboard')

    if status in ['confirmed', 'cancelled', 'completed']:
        appointment.status = status
        appointment.save()
        messages.success(request, f'Appointment status updated to {status}.')

    return redirect('appointment_detail', pk=pk)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        return redirect('patient_dashboard')
    return redirect('login')
