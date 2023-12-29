from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
import openai
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def analyze_texte(texte :str):
#     mot_cle=nltk.word_tokenize(texte)
#     return {"sujet":"vide","sentiments":[],"mot_cles":mot_cle}

# def generer_reponse(texte: str):
#     return {"reponse":"reponse vide"}

# def formater_reponse(texte: str):
#     return {"reponse_formater":"reponse vide formater"}



class AnalyseTexteInput(BaseModel):
    texte: str



@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    print(analyse_input)
    #miniscule
    texte=(analyse_input.texte).lower()
    #ponctuation
    
    translation_table = str.maketrans("", "", string.punctuation)
    text_clean= texte.translate(translation_table)

    #tokenisation
    tokens=nltk.word_tokenize(text_clean)
    print(tokens)

    #stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    print(tokens)
    #Lemmatization
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
    print(lemmatized_words)
    query=" ".join(lemmatized_words)+ " In context of Computer Science"
    print(query)
    response=Query_OpenIA(query)
    return {"msg": response}

def Query_OpenIA(query:str):
    

    openai.api_key = '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'
    conversation = "You are a computer science university teacher spcialized in AI, machine learning and deeplearning..explain "+ query
     
    response = openai.Completion.create(
    engine="gpt-3.5-turbo",  
    prompt=conversation,
    max_tokens=150
    )


    msg = response['choices'][0]['text']
    return msg

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)