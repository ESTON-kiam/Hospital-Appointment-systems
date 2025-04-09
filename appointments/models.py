from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    bio = models.TextField(blank=True)
    available_days = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Dr. {self.user.get_full_name()}'


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    blood_group = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Appointment #{self.id} - {self.patient} with {self.doctor}'


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medicine = models.TextField()
    dosage = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prescription for {self.appointment}'