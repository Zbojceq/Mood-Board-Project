document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Login button clicked.\nUsername: ' + document.getElementById('username').value);
});

document.getElementById('register').addEventListener('click', function() {
    alert('Redirect to Registration Page');
});

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
