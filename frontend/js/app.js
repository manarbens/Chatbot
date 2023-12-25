var BTN = document.querySelector(".btn-danger");
var TEXTAREA = document.querySelector("#textSpeech");
var DIV = document.querySelector("#reponse");
var BTN_MIC = document.querySelector("#sendButton");
var BTN_SEND = document.querySelector(".btn-danger");

// Check for Web Speech API support
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    var recognition = 'SpeechRecognition' in window ? new window.SpeechRecognition() : new window.webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    // Event Listeners
    BTN_SEND.addEventListener("click", chatBot);
    BTN_MIC.addEventListener("click", speechToText);

    // Function to handle chatBot logic
    function chatBot() {
        let text = TEXTAREA.value;
        communicateWithBackend(text);
    }

    // Function to handle speech-to-text
    function speechToText() {
        alert("Je suis speech to text");
        recognition.start();
    }

    // Event handler for recognition results
    recognition.onresult = function (event) {
        var message = event.results[0][0].transcript;
        console.log('Result received: ' + message + '.');
        console.log('Confidence: ' + event.results[0][0].confidence);
        TEXTAREA.value = message;
    };
} else {
    console.error('Web Speech API is not supported in this browser');
}

// Function to communicate with the backend
function communicateWithBackend(text) {
    var url_backend = "http://127.0.0.1:5500/analyse";
    fetch(url_backend, {
        method: "POST",
        body: JSON.stringify({ "texte": text }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data received from the server:', data);
        if (data && data.reponse) {
            console.log('OpenAI Response:', data.reponse);
            DIV.innerHTML = data.reponse;
        } else {
            console.error("Invalid or missing response from the server");
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
    });
}
