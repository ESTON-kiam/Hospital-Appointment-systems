from django.contrib import admin  # Correct import
from django.urls import include, path
from appointments.views import home

urlpatterns = [
    path('admin/', admin.site.urls),  # This now uses Django's admin
    path('', home, name='home'),
    path('', include('appointments.urls')),
]