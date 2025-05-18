
let calendar;
let monthYear;
let currentDate = new Date();
const today = new Date();

document.addEventListener("DOMContentLoaded", () => {
  calendar = document.getElementById("calendar");
  monthYear = document.getElementById("monthYear");
  renderCalendar(currentDate);
});

function renderCalendar(date) {
  calendar.innerHTML = "";
  const year = date.getFullYear();
  const month = date.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const startDay = (firstDayOfMonth + 6) % 7; // shift JS Sunday=0 to Monday=0

  monthYear.textContent = date.toLocaleString("pl-PL", {
    month: "long",
    year: "numeric",
  });

  
    fetch("data.json").catch(err => {
      console.error('Błąd ładowania danych:', err);
      document.getElementById("calendar").innerHTML = '<p style="color:red;">Błąd ładowania danych</p>';
    })
    
    .then((response) => response.json())
    .then((data) => {
      for (let i = 0; i < startDay; i++) {
        const empty = document.createElement("div");
        empty.className = "calendar-day";
        calendar.appendChild(empty);
      }

      for (let i = 1; i <= daysInMonth; i++) {
        const dateStr = `${year}-${(month + 1)
          .toString()
          .padStart(2, "0")}-${i.toString().padStart(2, "0")}`;
        const mood = data[dateStr]?.mood;
        const note = data[dateStr]?.note;

        const div = document.createElement("div");
        div.className = "calendar-day";

        const isToday =
          year === today.getFullYear() &&
          month === today.getMonth() &&
          i === today.getDate();

        if (isToday) div.classList.add("today");

        if (mood) {
          const colors = {
            happy: "#d0f5c0",
            sad: "#cfe3f9",
            angry: "#f7c2c2",
            anxious: "#ffe3b3",
            calm: "#e2ffe9",
            excited: "#fddff1",
            tired: "#ddd7f3",
            neutral: "#e4e4e4",
          };
          const emojis = {
            happy: "😊",
            sad: "😢",
            angry: "😠",
            anxious: "😰",
            calm: "😌",
            excited: "🤩",
            tired: "😴",
            neutral: "😐",
          };
          div.style.background = colors[mood] || "#eee";
          div.innerHTML = i + '<div class="emoji">' + (emojis[mood] || "") + "</div>";
          if (note) div.title = note;
        } else {
          div.textContent = i;
        }

        calendar.appendChild(div);
      }
    });
}

function prevMonth() {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar(currentDate);
}

function nextMonth() {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar(currentDate);
}

// Wykresy i czat
new Chart(document.getElementById("moodChart"), {
  type: "doughnut",
  data: {
    labels: ["Pozytywne", "Negatywne"],
    datasets: [
      {
        data: [12, 5],
        backgroundColor: ["#a3e635", "#f87171"],
      },
    ],
  },
});

new Chart(document.getElementById("moodLineChart"), {
  type: "line",
  data: {
    labels: ["1.05", "2.05", "3.05", "4.05", "5.05", "6.05", "7.05"],
    datasets: [
      {
        label: "Poziom nastroju (1-5)",
        data: [4, 3, 2, 5, 4, 1, 3],
        fill: false,
        borderColor: "#6c63ff",
        tension: 0.1,
      },
    ],
  },
});

lottie.loadAnimation({
  container: document.getElementById("notificationAnim"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "https://lottie.host/8c674f5f-78de-4f76-bb4e-0501f55da075/i6zjHDJZcJ.json",
});

function sendMessage() {
  const input = document.getElementById('chatMessage');
  const chatbox = document.getElementById('chatbox');
  if (input.value.trim()) {
    const div = document.createElement('div');
    div.className = 'chat-message';
    div.textContent = 'Ja: ' + input.value;
    chatbox.appendChild(div);
    input.value = '';
    chatbox.scrollTop = chatbox.scrollHeight;
  }
}
