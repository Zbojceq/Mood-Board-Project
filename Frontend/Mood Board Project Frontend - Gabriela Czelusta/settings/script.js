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
