
// Lottie Animations Setup
let lottie1 = document.getElementById('lottie1');
let lottie2 = document.getElementById('lottie2');
let lottie3 = document.getElementById('lottie3');

// Load Lottie Animations
lottie.loadAnimation({
    container: lottie1,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/c13cf2fd-8d2e-4afa-ae8b-4869c33a0ea1/LVjjmt0qpH.json' // Animation for "Connections"
});

lottie.loadAnimation({
    container: lottie2,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/185f0433-0e04-42d3-a020-19e613bece98/8L50wqvKhd.json' // Animation for "Person Details"
});

lottie.loadAnimation({
    container: lottie3,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/dd8ad16a-8fef-4500-83e0-f36118162202/F7LEhPNVY5.json' // Updated animation for "Notifications"
});

// Toggle expandable sections
const expandables = document.querySelectorAll('.expandable');

expandables.forEach(expandable => {
    expandable.addEventListener('click', () => {
        expandable.classList.toggle('active');
    });
});

// Event listeners for buttons
const sendInvitationBtn = document.getElementById('sendInvitationBtn');
const acknowledgeBtn = document.getElementById('acknowledgeBtn');
const backBtn = document.getElementById('backBtn');

// Action for sending invitation
sendInvitationBtn.addEventListener('click', () => {
    alert('Invitation sent!');
});

// Action for acknowledging mood change
acknowledgeBtn.addEventListener('click', () => {
    alert('Mood change acknowledged!');
});

// Action for "Back" button
backBtn.addEventListener('click', () => {
    window.history.back();
});
