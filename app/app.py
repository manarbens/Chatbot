from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from model import chat_with_gpt3
from time import sleep
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Téléchargez les ressources nécessaires pour NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

# Initialize an empty thread with the initial message
thread = ["Chatbot: Hello, how can I assist you today?"]

def preprocess_nlp(text):
    # Tokenisation
    tokens = word_tokenize(text.lower())
    
    # Suppression des stop words et des signes de ponctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    # Lemmatisation des tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Concaténation avec un espace et ajout de la phrase spécifiée
    preprocessed_text = ' '.join(tokens) + ' should be Tunisian recipe'
    
    return preprocessed_text

# Update your Flask route function
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    sleep(2)
    bot_response = None  # Initialize bot_response variable

    if request.method == 'POST':
        file1 = request.form['file1']
        print("Texte d'origine:", file1)
        preprocessed_text = preprocess_nlp(file1)
        print("Texte après prétraitement:", preprocessed_text)
        user_message = "You (Preprocessed): " + preprocessed_text
        thread.append(user_message)
        prompt = f"User: {preprocessed_text}\nChatbot:"
        chatbot_response = chat_with_gpt3(prompt)
        thread.append("Chatbot: " + chatbot_response)

        # Set bot_response for use in the template
        bot_response = chatbot_response

    return render_template('index.html', thread=thread, bot_response=bot_response)


if __name__ == "__main__":
    app.run(debug=True)
