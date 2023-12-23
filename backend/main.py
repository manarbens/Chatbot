from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from textblob import TextBlob

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_texte(texte :str):
    mot_cle=nltk.word_tokenize(texte)
    return {"sujet":"vide","sentiments":[],"mot_cles":mot_cle}

def generer_reponse(texte: str):
    return {"reponse":"reponse vide"}

def formater_reponse(texte: str):
    return {"reponse_formater":"reponse vide formater"}



class AnalyseTexteInput(BaseModel):
    texte: str



@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    print(analyse_input)
    #miniscule
    texte=(analyse_input.texte).lower()
    #ponctuation
    texte = ' '.join([char for char in texte if char not in string.punctuation])
    #texte.translate(str.maketrans("", "", string.punctuation))

    #erreur:Faute d'orthographe
    """blob = TextBlob(texte)
    texte = blob.correct()
    print(texte.words)
    print(type(texte.words))"""

    #tokenisation
    tokens=nltk.word_tokenize(texte)
    print(tokens)

    #stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    print(tokens)


    

    #Stemmer & Lemmatization
    
    #porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    #stemmed_words = [porter.stem(word) for word in tokens]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
    print(lemmatized_words)

    return {"msg": analyse_input}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)