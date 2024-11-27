document.getElementById('translate-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const text = document.getElementById('text-to-translate').value;
    const language = document.getElementById('language-select').value;

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text, language: language })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('translated-text').innerText = `Translated Text: ${data.translated_text}`;
        } else {
            console.error('Error:', data);
            document.getElementById('translated-text').innerText = 'Translation failed';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('translated-text').innerText = 'Translation failed';
    }
});

document.getElementById('identify-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const text = document.getElementById('text-to-identify').value;

    try {
        const response = await fetch('/api/identify_language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('identified-language').innerText = `Identified Language: ${data.language}`;
        } else {
            console.error('Error:', data);
            document.getElementById('identified-language').innerText = 'Language identification failed';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('identified-language').innerText = 'Language identification failed';
    }
});
