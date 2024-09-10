import streamlit as st
import pandas as pd
import requests
 
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

# Diese Modul wird verwendet um Projekt Gutenberg zu scrapen
# Verschiedene Funktionalität für die einzelnen Seiten (Autoren, Buch) wird zur Verfügung gestellt

# Die Start-URL für alle Anfragen
BASE_URL = "https://www.projekt-gutenberg.org"


@st.cache_resource
def scrape_autor(author): # Only Function that should be accessed from outside the modul
    """ 
    Extrahiert alle Informationen über den Autor 'author' in Projekt Gutenberg. 

    Parameters:
        author (str): Der Name des Autors

    Returns:
        dic (dict): Ein Wörterbuch mit allen relevanten Informationen zum Autor
    """

    url = f"{BASE_URL}/autoren/namen/{author.lower()}.html"
    
    print(f"Scrape Autor {author} [{url}]")
    
    res = requests.get(url) 
    
    # Autor nicht gefunden
    if res.status_code != 200:
        print(f"Autor {author} wurde nicht gefunden.")
        return None
    
    # Scraping mit BeautifulSoup
    try:
        print(f"Autor {author} wurde gefunden.")
        author_site = BeautifulSoup(res.content, 'lxml', from_encoding= EncodingDetector.find_declared_encoding(res.content, is_html=True))
    
    # Decoding Fehler
    except Exception:
        print("Error while decoding page")
        return None

    # Wörterbuch mit den extrahierten Informationen
    infos = {"data"  : None, 
             "books" : _find_books(author_site), 
             "info"  : _find_info(author_site), 
             "image_url" : _find_image(author_site)
            }
    
    df_all = pd.DataFrame()

    # Text aller Bücher
    for title, url in infos["books"]:  

        st.markdown(f"[{title}]({url})")
        print(f"Scrape Buch '{title}' [{url}]")

        # Das Buch scrapen
        df_temp = _scrape_book(url)

        # Die Dataframes kombinieren            
        df_all = pd.concat([df_all,df_temp], ignore_index=True)
            
    df_all["Autor"] = author.upper()
    
    infos["data"] = df_all
    
    print(f"Gefundene Sätze: {df_all.shape}")
    
    return infos
    


def _scrape_book(url):
    """
    Führt das Scrapen des Buches aus der URL aus.
    
    Parameters:
        url (str): Die Addresse des Buches
        
    Returns:
        df (DataFrame): Ein DataFrame mit allen Sätzen
    """
    res = requests.get(url) 

    book_site = BeautifulSoup(res.content, 'lxml', from_encoding=EncodingDetector.find_declared_encoding(res.content, is_html=True))

    subchapters = book_site.find_all("li")
    
    print(f"\tAnzahl Unterkapitel: {len(subchapters)}")

    subchapters_links = []
  
    for sub in subchapters:
        link = sub.find("a", href=True)
        subchapters_links.append(url + "/" + link["href"]) 
    
    df = pd.DataFrame(columns=["Satz"])
    
    progressbar = st.progress(0)
    
    for index, temp_url in enumerate(subchapters_links):

        # Zeige die Progressbar an
        progressbar.progress((index+1)/len(subchapters_links))

        res = requests.get(temp_url) 
        books = BeautifulSoup(res.content, 'lxml', from_encoding=EncodingDetector.find_declared_encoding(res.content, is_html=True))

        data = _find_text(books)
        
        for satz in data.split("."):
            df.loc[len(df)] = satz

    # Löschen der ProgressBar
    progressbar.empty()    
    
    df["Satz"] = df["Satz"].map(_correction).dropna()
    
    return df


def _find_image(author_site):
    """
    Extrahiert den Link zum Autorenbild aus dem Quellcode für eine Autorenseite, 
    siehe z.B. den HTML-Code von:  https://www.projekt-gutenberg.org/autoren/namen/kafka.html
    
    Falls ein Bild gefunden wurde, wird die URL zurückgegeben.
    
    Parameters:
        books (str): Der HTML-Code der Bücher, die vom Autor geschrieben sind

    Returns:
        Die Addresse des Bildes oder None
    """
    try:
        return f"{BASE_URL}/autoren/{author_site.find('img', src=True, title=True)['src'][3:]}"
        
    except:
        return None

def _find_info(author_site):
    """ 
    Extrahiert Informationen über den Autor aus dem Quellcode für eine Autorenseite, 
    siehe z.B. https://www.projekt-gutenberg.org/autoren/namen/kafka.html

    Falls Informationen gefunden wurden, werden diese als Text zurückgegeben.   
    
    Parameters:
        books (str): Der HTML-Code der Bücher, die vom Autor geschrieben sind

    Returns:
        Alle Paragraphe oder None
    """
    try:
        return author_site.find_all("p")[1].text
    
    except:
        return None



def _find_text(books):
    """ 
    Liefert den Text eines Onlinebuches, was schon durch BeautifulSoup geparst ist.

    Parameters:
        books (dict): Der HTML-Code aller Bücher 
        
    Returns:
        text (str): Der String mit allen Texten
    """
    
    
    text = ""
    
    # Findet alle HTML Paragraphe mit dem Tag <\p>
    for paragraph in books.find_all("p"):
        
        if paragraph.string:
         
            text += paragraph.text             
    
    return text


def _find_books(books):
    """ 
    Liefert alle Bücher, die der Autor geschrieben hat.

    Parameters:
        books (str): Der HTML-Code der Bücher, die vom Autor geschrieben sind
        
    Returns:
        book_url (list): Eine Liste von Tupels des Titels und der URL
    """    
    tag = books.find("div", {"class":"archived"})
    
    if tag == None:
        return []
    
    book_url = []
    
    # Die Bücher findet man unter der Liste mit dem Tag <li>
    for l in tag.find_all("li"):

        tag = l.find("a",href=True)
        
        book_title = tag.string
        
        url = f"{BASE_URL}/{tag['href'][6:]}"
        url = url[:url.rfind("/")]
        
        book_url.append((book_title, url))
        
    return book_url


def _correction(string):
    """ 
    Die Funktion filtert Sätze die kleiner als 4 Zeichen sind aus der Analyse.
    Ergänzbar um weitere Kriterien.
    
    Parameters:
        string (str): Der Satz zum filtern
        
    Returns:
        Entweder den String oder None. 
    """
    if len(string)< 4: 
        return None

    else:
        return string