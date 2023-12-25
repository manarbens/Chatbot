from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from model import chat_with_gpt3
from time import sleep

# Téléchargez les ressources nécessaires pour NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)



start = ["Chatbot: Hello, how can I assist you today?"]
thread=[]
@app.route('/')
def home():
    thread=[]
    return render_template('index.html',thread = start) 

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


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    sleep(2)
    if request.method == 'POST':
        file1 = request.form['file1']
        
        # Affiche le texte d'origine
        print("Texte d'origine:", file1)
        
        # Ajout du prétraitement NLP
        preprocessed_text = preprocess_nlp(file1)
        
        # Affiche le texte après prétraitement
        print("Texte après prétraitement:", preprocessed_text)
        
        thread.append("You (Preprocessed): " + preprocessed_text)
        
        prompt = f"User: {preprocessed_text}\nChatbot:"
        chatbot_response = chat_with_gpt3(prompt)
        thread.append("Chatbot: " + chatbot_response)

    return render_template('index.html', thread=thread)



if __name__ == "__main__":
    app.run(debug=True)