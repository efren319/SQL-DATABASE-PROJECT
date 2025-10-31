// Form Validation and Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to tables
    const tables = document.querySelectorAll('table');
    tables.forEach(table => table.classList.add('fade-in'));

    // Validate and handle feedback form
    const feedbackForm = document.querySelector('#feedback-form');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            const name = document.querySelector('#name').value.trim();
            const comment = document.querySelector('#comment').value.trim();
            if (!name || !comment) {
                alert('Please fill in all fields.');
                e.preventDefault();
                return;
            }
            if (!confirm('Submit your feedback?')) {
                e.preventDefault();
            } else {
                // Simulate success message (in a real app, handle via AJAX)
                setTimeout(() => alert('Feedback submitted successfully!'), 100);
            }
        });
    }

    // Validate and handle upload form
    const uploadForm = document.querySelector('#upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const dept = document.querySelector('#department').value.trim();
            const allocated = parseFloat(document.querySelector('#allocated').value);
            const spent = parseFloat(document.querySelector('#spent').value);
            if (!dept || isNaN(allocated) || isNaN(spent) || allocated < 0 || spent < 0) {
                alert('Please enter valid data for department, allocated, and spent amounts.');
                e.preventDefault();
                return;
            }
            if (spent > allocated) {
                alert('Spent amount cannot exceed allocated amount.');
                e.preventDefault();
                return;
            }
            if (!confirm('Update the data?')) {
                e.preventDefault();
            }
        });
    }

    // Dynamic feedback display (optional enhancement)
    const feedbackList = document.querySelector('#feedback-list');
    if (feedbackList) {
        // In a real app, use AJAX to fetch new feedback without reload
        // For now, just ensure it's visible
        feedbackList.style.display = 'block';
    }
});