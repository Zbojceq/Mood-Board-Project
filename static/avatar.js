// Set up the canvas
const canvas = document.getElementById('avatarCanvas');
const ctx = canvas.getContext('2d');

// Initial Avatar Settings
let headColor = '#fbbf24'; // Yellow head color
let eyesColor = '#000000'; // Black eyes color
let mouthColor = '#e11d48'; // Red mouth color

// Draw the initial avatar with animation
function drawAvatar() {
    // Clear canvas before drawing
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the head with a smooth animation
    ctx.fillStyle = headColor;
    ctx.beginPath();
    ctx.arc(200, 150, 80, 0, Math.PI * 2, true); // Head
    ctx.fill();

    // Draw the eyes
    ctx.fillStyle = eyesColor;
    ctx.beginPath();
    ctx.arc(160, 120, 15, 0, Math.PI * 2, true); // Left eye
    ctx.arc(240, 120, 15, 0, Math.PI * 2, true); // Right eye
    ctx.fill();

    // Draw the mouth
    ctx.fillStyle = mouthColor;
    ctx.beginPath();
    ctx.arc(200, 180, 50, 0, Math.PI, false); // Mouth
    ctx.fill();
}

// Change color function using the palette
function changeColor(part, color) {
    if (part === 'head') {
        headColor = color;
    } else if (part === 'eyes') {
        eyesColor = color;
    } else if (part === 'mouth') {
        mouthColor = color;
    }

    drawAvatar(); // Redraw the avatar with new colors
}

// Clear canvas with animation
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawAvatar(); // Redraw with default colors
}

// Save the avatar as an image
function saveAvatar() {
    const dataUrl = canvas.toDataURL("image/png");
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = 'avatar.png';
    link.click();
}

// Initial drawing
drawAvatar();
