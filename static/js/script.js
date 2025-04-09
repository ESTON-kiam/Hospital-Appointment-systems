document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Date picker initialization for appointment date
    if (document.getElementById('id_date')) {
        document.getElementById('id_date').type = 'date';
    }

    // Time picker initialization for appointment time
    if (document.getElementById('id_time')) {
        document.getElementById('id_time').type = 'time';
    }

    // Doctor availability check (would need to be implemented with AJAX)
    // This is just a placeholder for the actual implementation
    if (document.getElementById('id_doctor')) {
        document.getElementById('id_doctor').addEventListener('change', function() {
            // Here you would fetch the doctor's available days/times
            console.log('Doctor selected:', this.value);
        });
    }
});