document.getElementById('forgot').addEventListener('click', function() {
    alert('Redirect to Password Recovery');
});

document.getElementById('goToApp').addEventListener('click', function() {
    alert('Entering the Application...');
});
// MODAL - Forgot Password
document.getElementById('forgot').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('passwordModal').style.display = "flex";
});

// Zamknij modal
document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('passwordModal').style.display = "none";
});

// Wyślij link
document.getElementById('sendLink').addEventListener('click', function() {
    const email = document.getElementById('recoveryEmail').value;
    if (email) {
        alert(`Password reset link sent to ${email}`);
        document.getElementById('passwordModal').style.display = "none";
    } else {
        alert("Please enter a valid email address.");
    }
});

// Remember Me button logic
const rememberBtn = document.getElementById('rememberMeBtn');
const rememberCheckbox = document.querySelector('.remember-checkbox');
if (rememberBtn && rememberCheckbox) {
    // Always start as FALSE (unchecked, greyed out)
    rememberBtn.classList.remove('selected');
    rememberCheckbox.checked = false;
    rememberBtn.textContent = 'Remember Me: OFF';

    rememberBtn.addEventListener('click', function() {
        const isSelected = rememberBtn.classList.toggle('selected');
        rememberCheckbox.checked = isSelected;
        rememberBtn.textContent = isSelected ? 'Remember Me: ON' : 'Remember Me: OFF';
    });
}
