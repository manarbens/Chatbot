var BTN = document.querySelector("#bText");
var TEXTAREA = document.querySelector("#textSpeech");
var DIV = document.querySelector("#response_msg");

var BTN_MIC = document.querySelector("#bMic");
var BTN_SP = document.querySelector("#bSpeak");

var recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

// Declare data in a higher scope
var data;

// Use Web Speech API for text-to-speech
BTN_SP.addEventListener("click", function (event) {
    event.preventDefault();
    // Check if data is defined before calling startTextToSpeech
    if (data) {
        startTextToSpeech(data.msg);
    }
});

// EVENEMENT
BTN.addEventListener("click", chatBot);
BTN_MIC.addEventListener("click", speechToText);

// fonction principale
function chatBot() {
    let text = TEXTAREA.value;

    // je dois communiquer avec le backend
    var url_backend = "http://127.0.0.1:8001/analyse";
    fetch(url_backend, {
        method: "POST",
        body: JSON.stringify({ "texte": text }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(reponse => {
        reponse.json()
            .then(receivedData => {
                data = receivedData; // Assign received data to the outer variable
                BTN_SP.style.display = "";

                BTN_SP.addEventListener("click", function () {
                    texteToSpeech(data.msg);
                });

                console.log(data.msg);
                // Format the bot's response in a green rectangle
                var botMessageHTML = `<div class="message bot-message">${data.msg}</div>`;
                DIV.innerHTML += botMessageHTML;
            })
    })
    .catch(e => {
        console.warn(e);
    });
}

function speechToText() {
    recognition.start();
}

function startTextToSpeech(texte) {
    console.log('startTextToSpeech called with text:', texte);
    const speechOutput = new SpeechSynthesisUtterance();
    speechOutput.text = texte;

    // Set language to English
    speechOutput.lang = 'en-US'; // or 'en'

    speechSynthesis.speak(speechOutput);
}

recognition.onresult = function (event) {
    var message = event.results[0][0].transcript;
    console.log('Result received: ' + message + '.');
    console.log('Confidence: ' + event.results[0][0].confidence);
    TEXTAREA.value = message;
}