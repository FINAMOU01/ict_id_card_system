// ICT University Student ID System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form validation for registration
    const registerForm = document.querySelector('form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const matricule = document.getElementById('matricule').value.trim();
            const fullName = document.getElementById('full_name').value.trim();
            const photo = document.getElementById('photo').files[0];

            let isValid = true;
            let errorMessage = '';

            if (!fullName) {
                errorMessage += 'Full Name is required.\n';
                isValid = false;
            }

            if (!matricule) {
                errorMessage += 'Matricule is required.\n';
                isValid = false;
            }

            if (!photo) {
                errorMessage += 'Student photo is required.\n';
                isValid = false;
            } else {
                // Check file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
                if (!allowedTypes.includes(photo.type)) {
                    errorMessage += 'Please upload a valid image file (JPEG, JPG, PNG).\n';
                    isValid = false;
                }
                // Check file size (max 5MB)
                if (photo.size > 5 * 1024 * 1024) {
                    errorMessage += 'Image file size must be less than 5MB.\n';
                    isValid = false;
                }
            }

            if (!isValid) {
                e.preventDefault();
                alert(errorMessage);
            }
        });
    }

    // Download button functionality
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Optional: Add loading state or confirmation
            this.textContent = 'Downloading...';
            this.disabled = true;
            // Re-enable after a short delay (in real app, handle in response)
            setTimeout(() => {
                this.textContent = this.textContent.replace('Downloading...', 'Download ' + (this.href.includes('pdf') ? 'PDF' : 'PNG'));
                this.disabled = false;
            }, 2000);
        });
    });
});