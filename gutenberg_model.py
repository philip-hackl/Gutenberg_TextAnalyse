import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

def analyze(data):
    
    df = pd.DataFrame()
    
    for a in data.values():
        df = pd.concat([df, a["data"]], ignore_index=True)
    df= df.dropna()
    vect = CountVectorizer()
    wordsCountArray = vect.fit_transform(df["Satz"])

    # Train Test Daten aufteilen    
    X_train, X_test, y_train, y_test = train_test_split(wordsCountArray, df["Autor"], test_size=0.2, random_state=0)

    # Model trainieren
    model = MultinomialNB()
    model.fit(X_train, y_train)

    autoren = data.keys()
   
    s = f"Modell trainiert für Autoren: \n\n"
    
    for autor in autoren:
        s += f"\t{autor}\n"
    
    s += f"Mit {X_train.shape[0]} Sätzen.\n\n"
    s += f"Modelgenauigkeit: {model.score(X_test,y_test) *100:.2f}%"
    
    st.markdown(s)
    
    return model, vect