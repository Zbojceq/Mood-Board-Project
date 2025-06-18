// Obsługa kliknięcia przycisku "Powrót"
document.getElementById("backButton").addEventListener("click", function() {
    window.history.back(); // Wróć do poprzedniej strony
});

// Wyślij zaproszenie
document.getElementById("sendInvite").addEventListener("click", function() {
    const inviteId = document.getElementById("inviteId").value;
    if (inviteId) {
        alert("Zaproszenie wysłane do: " + inviteId);
        addPendingInvite(inviteId);
    } else {
        alert("Proszę podać ID lub e-mail.");
    }
});

// Dodawanie grupy
document.getElementById("groupCreateButton").addEventListener("click", function() {
    const groupName = document.getElementById("groupName").value;
    if (groupName) {
        alert("Grupa " + groupName + " została stworzona!");
        document.getElementById("groupName").value = '';  // Wyczyść pole po dodaniu
    } else {
        alert("Proszę podać nazwę grupy.");
    }
});

// Przełączanie sekcji grup
function toggleGroupSection() {
    const groupSection = document.querySelector(".group-section");
    groupSection.classList.toggle("show");
}

// Akceptowanie zaproszenia
function acceptInvite(inviteElement, inviteId) {
    alert("Zaproszenie od " + inviteId + " zaakceptowane.");
    addConnectedPerson(inviteId);
    inviteElement.remove();
}

// Odrzucenie zaproszenia
function rejectInvite(inviteElement) {
    alert("Zaproszenie odrzucone.");
    inviteElement.remove();
}

// Funkcja do dodania połączonej osoby
function addConnectedPerson(personId) {
    const connectedPeopleContainer = document.getElementById("connectedPeople");
    const personElement = document.createElement("div");
    personElement.textContent = personId + " - Partner";
    connectedPeopleContainer.appendChild(personElement);
}
