var BTN = document.querySelector("button");
var TEXTAREA = document.querySelector("#textSpeech");
var DIV = document.querySelector("#reponse_msg");
var BTN_MIC = document.querySelector("#bMic");

// Check for Web Speech API support
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    // Use the Web Speech API if available, otherwise use the webkitSpeechRecognition
    var recognition = 'SpeechRecognition' in window ? new window.SpeechRecognition() : new window.webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    // EVENT
    BTN.addEventListener("click", chatBot);
    BTN_MIC.addEventListener("click", speechToText);

    // Function for chatBot
    function chatBot() {
        let text = TEXTAREA.value;

        // Communicate with the backend
        var url_backend = "http://127.0.0.1:8001/analyse";
        fetch(url_backend, {
            method: "POST",
            body: JSON.stringify({
                "texte": text
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(reponse => {
            reponse.json()
            .then(data => {
                console.log(data.msg);
                DIV.innerHTML = data.msg;
            });
        })
        .catch(e => {
            console.warn(e);
        });
    }

    // Function for speechToText
    function speechToText() {
        alert("Je suis speech to text");
        // Trigger the Speech Recognition API
        recognition.start();
    }

    // Event handler for recognition results
    recognition.onresult = function (event) {
        // Get the recognized text
        var message = event.results[0][0].transcript;
        console.log('Result received: ' + message + '.');
        console.log('Confidence: ' + event.results[0][0].confidence);

        // Fill the input with the recognized text
        TEXTAREA.value = message;
    };
} else {
    // Web Speech API is not supported in this browser
    console.error('Web Speech API is not supported in this browser');
}
