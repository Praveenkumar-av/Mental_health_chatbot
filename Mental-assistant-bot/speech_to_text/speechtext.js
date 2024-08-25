document.getElementById('speechButton').addEventListener('click', function () {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support speech recognition.');
        return;
    }

    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.interimResults = true;

    recognition.addEventListener('result', (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');

        document.getElementById('text').value = transcript;
    });

    recognition.addEventListener('end', () => {
        console.log('Speech recognition ended.');
    });

    recognition.start();
});