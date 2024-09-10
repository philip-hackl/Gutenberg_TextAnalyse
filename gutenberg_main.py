#Startpunkt
# Navigiere zum Ordner

# Start with:
# streamlit run gutenberg_main.py

import streamlit as st

from gutenberg_scraping import scrape_autor
from gutenberg_model import analyze

st.set_page_config(layout="wide") 

# Titel
st.header("[Projekt Gutenberg](https://www.projekt-gutenberg.org) (Prototyp)")
col1, col2 = st.columns(2)    

# st.session_state speichert alle Daten, die über die Session erhalten werden sollen.
# Alle anderen Daten werden bei einem automatischen Neuladen der Seite gelöscht.

if "vect" not in st.session_state:   
    # Der Vectorizer für unser Model (https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)
    st.session_state.vect = None

if "model" not in st.session_state:
    # Das Modell, ein Naive Bayes (https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB)
    st.session_state.model = None

if "data" not in st.session_state:
    # Die gescrapten Informationen über die Autoren als Wörterbuch. (siehe return value von scrape_autor)
    st.session_state.data = {}


# Autor Sidebar
autor = st.sidebar.text_input("Welche*r Autor*in interessiert dich?", value="Kafka", help="Der Nachname ist ausreichend.").upper()

st.sidebar.markdown("""Durch die Verwendung der [session_state](https://docs.streamlit.io/library/api-reference/session-state) werden die Daten eines Autors nur **einmal** gescrapt. 
Bei nochmaliger Abfrage werden automatisch die schon existierenden Daten geladen.""")

if st.sidebar.button("Starte Scraping...", help="Extrahiert die Informationen über die ausgewählte Person von Projekt Gutenberg."):
    

    #Befindet sich der Autor noch nicht in der Session_state ?
    if autor not in st.session_state.data.keys():
        
        # Scrape Autor
        data = scrape_autor(autor)
    
        if data == None:
            st.error("Abfrage fehlerhaft.")
    
        else:
            st.session_state.data[autor.upper()] = data
    
    else:
        print("Autor*in wurde schon extrahiert.")

if st.sidebar.button("Lösche Daten", disabled=len(st.session_state.data.keys())==0, help=f"Löscht alle extrahierten Daten"):
    st.session_state.data = {}


# Spalte um Informationen über den Autor auszugeben     
with col1:
    
    if autor in st.session_state.data.keys():
        
        st.subheader("Biographie")
        st.write(st.session_state.data[autor.upper()]["info"])

        if st.session_state.data[autor.upper()]["image_url"]:
            st.image(st.session_state.data[autor.upper()]["image_url"])
    
        st.dataframe(st.session_state.data[autor.upper()]["data"],width=600)
        
        st.subheader("Bücher")
        
        for b in st.session_state.data[autor.upper()]["books"]:
            st.markdown(f"[{b[0]}]({b[1]})") 


# Spalte für Datascience          
with col2:
  
    selection = st.multiselect("Autoren", st.session_state.data.keys())

    analyse = st.button("Analysiere ausgewählte Autoren", help="Erstellt ein Modell mit den ausgewählten Autoren.")

    if analyse and selection!= []:
        m={}    

        for sel in selection:
            m[sel] = st.session_state.data[sel]
        
        if m!={}:
            st.session_state.model, st.session_state.vect = analyze(m)

    text = st.text_input("Wer hat es (wahrscheinlich) geschrieben?" )

    if st.session_state.model != None and st.session_state.vect != None:
        propas = st.session_state.model.predict_proba(st.session_state.vect.transform([text]))

        for i in range(len(st.session_state.model.classes_)):
            st.markdown(f"**{st.session_state.model.classes_[i]}**: {propas[0][i]*100:.2f} % ")