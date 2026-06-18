// Main JavaScript for CP Platform

// Close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-error')) {
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.3s';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        }
    });
});

// Format datetime inputs
function formatDatetime(datetime) {
    return new Date(datetime).toLocaleString();
}

// Confirmation dialogs
function confirmAction(message) {
    return confirm(message);
}

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    for (let input of inputs) {
        if (!input.value.trim()) {
            alert(`Please fill in: ${input.placeholder || input.name}`);
            return false;
        }
    }
    return true;
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// AJAX helpers
async function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };

    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        const data = await response.json();
        return { success: response.ok, data, status: response.status };
    } catch (error) {
        console.error('Request failed:', error);
        return { success: false, error: error.message };
    }
}

// Initialize tooltips or other interactive elements
function initializeUI() {
    // Add any interactive features here
    console.log('UI initialized');
}

// Export functions for use in templates
window.CP = {
    formatDatetime,
    confirmAction,
    validateForm,
    copyToClipboard,
    makeRequest,
    initializeUI
};
