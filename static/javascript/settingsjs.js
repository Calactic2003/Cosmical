document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const targetId = this.getAttribute('href').substring(1);
            document.querySelectorAll('.settings-section').forEach(section => {
                if (section.id === targetId) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        });
    });
    
    // Set initial active section
    document.querySelectorAll('.settings-section').forEach((section, index) => {
        if (index !== 0) {
            section.style.display = 'none';
        }
    });
    
    // Image preview functionality
    function setupImagePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                
                reader.addEventListener('load', function() {
                    preview.src = this.result;
                });
                
                reader.readAsDataURL(file);
            }
        });
    }
    
    setupImagePreview('profile-pic-upload', 'profile-pic-preview');
    setupImagePreview('banner-upload', 'banner-preview');
    
    // Password validation
    const form = document.getElementById('settings-form');
    const errorMessage = document.getElementById('error-message');
    
    form.addEventListener('submit', function(e) {
        // Validate password fields only
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        if (newPassword && newPassword !== confirmPassword) {
            e.preventDefault(); // Stop form submission
            errorMessage.textContent = 'New passwords do not match.';
            errorMessage.style.display = 'block';
            return false;
        }
        // Let the form submit normally to your Django view
    });
    
    // Connect social media accounts
    document.getElementById('connect-facebook')?.addEventListener('click', function() {
        window.location.href = '/auth/facebook/';
    });
    
    document.getElementById('connect-twitter')?.addEventListener('click', function() {
        window.location.href = '/auth/twitter/';
    });
    
    document.getElementById('connect-google')?.addEventListener('click', function() {
        window.location.href = '/auth/google/';
    });
});