// Preview avatar image when selected
function previewAvatar(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.id = "avatarPreview";
        document.querySelector("section#accountSettings").appendChild(img);
    };
    reader.readAsDataURL(file);
}

// Animacja rozwijanych sekcji
const sections = document.querySelectorAll("section");

sections.forEach((section) => {
    section.addEventListener("click", () => {
        section.classList.toggle("active");
    });
});

// Utility to mask email (show first 3 and last 3 chars)
function maskEmail(email) {
    if (!email || email.length < 7) return email;
    return email.slice(0, 3) + '...' + email.slice(-5);
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Fetch current user info and display
function loadAccountInfo() {
    fetch('/settings', { 
        method: 'POST', 
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        } 
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('current-username').textContent = 'Username: ' + data.username;
            document.getElementById('current-email').textContent = 'Email: ' + maskEmail(data.email);
        });
}

// Popup logic
function showPopup(id) {
    document.getElementById(id).style.display = 'flex';
}
function hidePopups() {
    document.querySelectorAll('.popup').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.popup-error').forEach(e => e.textContent = '');
}

document.addEventListener('DOMContentLoaded', function() {
    loadAccountInfo();
    document.getElementById('change-username-btn').onclick = () => showPopup('popup-username');
    document.getElementById('change-email-btn').onclick = () => showPopup('popup-email');
    document.getElementById('change-password-btn').onclick = () => showPopup('popup-password');
    document.querySelectorAll('.close-popup').forEach(btn => btn.onclick = hidePopups);

    // Username change
    document.getElementById('form-username').onsubmit = function(e) {
        e.preventDefault();
        const form = e.target;
        fetch('/settings', {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                action: 'change_username',
                password: form.password.value,
                new_username: form.new_username.value
            })
        }).then(res => res.json()).then(data => {
            if (data.success) {
                hidePopups();
                loadAccountInfo();
            } else {
                document.getElementById('error-username').textContent = data.error || 'Error';
            }
        });
    };
    // Email change
    document.getElementById('form-email').onsubmit = function(e) {
        e.preventDefault();
        const form = e.target;
        fetch('/settings', {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                action: 'change_email',
                password: form.password.value,
                new_email: form.new_email.value
            })
        }).then(res => res.json()).then(data => {
            if (data.success) {
                hidePopups();
                loadAccountInfo();
            } else {
                document.getElementById('error-email').textContent = data.error || 'Error';
            }
        });
    };
    // Password change
    document.getElementById('form-password').onsubmit = function(e) {
        e.preventDefault();
        const form = e.target;
        fetch('/settings', {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                action: 'change_password',
                old_password: form.old_password.value,
                new_password1: form.new_password1.value,
                new_password2: form.new_password2.value
            })
        }).then(res => res.json()).then(data => {
            if (data.success) {
                hidePopups();
            } else {
                document.getElementById('error-password').textContent = data.error || 'Error';
            }
        });
    };
    // Delete account popup
    document.getElementById('delete-account-btn').onclick = function() {
        showPopup('popup-delete-account');
    };
    document.getElementById('form-delete-account').onsubmit = function(e) {
        e.preventDefault();
        const form = e.target;
        const confirmText = form.confirm_text.value.trim().toLowerCase();
        const password = form.password.value;
        if (confirmText !== 'confirm') {
            document.getElementById('error-delete-account').textContent = "You must type 'confirm' to delete your account.";
            return;
        }
        fetch('/settings', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ password })
        }).then(res => res.json()).then(data => {
            if (data.success) {
                window.location.href = data.redirect || '/login';
            } else {
                document.getElementById('error-delete-account').textContent = data.error || 'Error deleting account';
            }
        });
    };
});
