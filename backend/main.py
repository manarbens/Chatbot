from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import openai
import creds
import os

os.environ["OPENAI_KEY"] = creds.API_KEY
openai.api_key = os.environ["OPENAI_KEY"]

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_texte(texte: str):
    mot_cle = nltk.word_tokenize(texte)
    return {"sujet": "vide", "sentiments": [], "mot_cles": mot_cle}

def generer_reponse(texte: str):
    return {"reponse": "reponse vide"}

def formater_reponse(texte: str):
    return {"reponse_formater": "reponse vide formater"}

class AnalyseTexteInput(BaseModel):
    texte: str

@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    print(analyse_input)
    # minuscule
    texte = (analyse_input.texte).lower()
    # ponctuation
    texte = ' '.join([char for char in texte if char not in string.punctuation])
    # tokenisation
    tokens = nltk.word_tokenize(texte)
    print(tokens)
    # stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    print(tokens)
    # Stemmer & Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
    print(lemmatized_words)
    query = " ".join(lemmatized_words) + " should be Tunisian recipe"
    print(query)

    # Now you can use the generated query with OpenAI API
    chat_prompt = [{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_prompt, max_tokens=200)
    print(response)

    if "choices" in response and response["choices"]:
        return {"reponse": response["choices"][0]["message"]["content"]}
    else:
        return {"reponse": "No valid response from OpenAI"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5500)
