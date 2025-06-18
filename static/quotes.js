const quoteText = document.getElementById('quote');
const authorText = document.getElementById('author');
const newQuoteBtn = document.getElementById('newQuote');
const saveAndHomeBtn = document.getElementById('saveAndHome');

async function getQuote() {
    quoteText.style.opacity = 0;
    authorText.textContent = '';

    try {
        // 👇 PODMIENISZ TU NA SWOJE API BACKEND
        // const response = await fetch('http://localhost:5000/random-quote');
        const response = await fetch('https://api.quotable.io/random');
        const data = await response.json();
        setTimeout(() => {
            quoteText.textContent = `"${data.content}"`;
            authorText.textContent = `— ${data.author}`;
            quoteText.style.opacity = 1;
        }, 200);
    } catch (error) {
        quoteText.textContent = 'Error. Try again.';
        quoteText.style.opacity = 1;
        authorText.textContent = '';
    }
}

getQuote();
newQuoteBtn.addEventListener('click', getQuote);

saveAndHomeBtn.addEventListener('click', () => {
    localStorage.setItem('lastQuote', quoteText.textContent);
    localStorage.setItem('lastAuthor', authorText.textContent);
    window.location.href = 'index.html';
});