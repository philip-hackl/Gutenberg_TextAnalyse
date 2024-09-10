# Gutenberg Author Text Analysis

## Projektbeschreibung

Dieses Projekt bietet eine interaktive Streamlit-Anwendung zur Analyse von Texten von Autoren des Gutenberg-Projekts. Benutzer können Autoren auswählen, deren Werke scrapen und analysieren lassen, und sogar eigene Texte eingeben, um die Wahrscheinlichkeit zu bestimmen, welchem Autor der Text zuzuordnen ist. Die Anwendung nutzt einfache und fortgeschrittene KI-Techniken zur Texterkennung und Klassifizierung.

## Inhaltsverzeichnis

1. [Projektbeschreibung](#projektbeschreibung)
2. [Installation](#installation)
3. [Verwendung](#verwendung)
   - [Starten der Anwendung](#starten-der-anwendung)
   - [Benutzeroberfläche](#benutzeroberfläche)
4. [Funktionen](#funktionen)
5. [Code Übersicht](#code-übersicht)
6. [Funktionsweise](#funktionsweise)
7. [Contributing](#contributing)



## Installation

Stelle sicher, dass du die benötigten Python-Pakete installiert hast. Du kannst diese mit `pip` installieren:

```bash
pip install streamlit pandas requests beautifulsoup4 scikit-learn
```

## Verwendung

### Starten der Anwendung

1. **Clone das Repository:**

    ```bash
    git clone https://github.com/philip-hackl/TicTacToe-Game.git
    ```

2. **Navigiere in das Projektverzeichnis:**

    ```bash
    cd TicTacToe-Game
    ```

3. **Starte die Streamlit-Anwendung:**

    ```bash
    streamlit run gutenberg_main.py
    ```

### Benutzeroberfläche

- **Autor-Suche:** Wähle den Namen eines Autors aus, um Informationen und Texte von Projekt Gutenberg zu scrapen. Die Eingabe des Nachnamens genügt.
- **Scraping starten:** Drücke auf den Button „Starte Scraping...“, um die Informationen des Autors herunterzuladen und anzuzeigen.
- **Daten löschen:** Du kannst alle gescrapten Daten über den Button „Lösche Daten“ entfernen.
- **Textanalyse:** Gebe einen Text ein, um zu bestimmen, welcher Autor mit einer bestimmten Wahrscheinlichkeit hinter dem Text stehen könnte. Wähle zuvor Autoren aus, die in der Analyse berücksichtigt werden sollen.

## Funktionen

1. **Scraping von Autoren:**
   - Holt Informationen zu Autoren von Projekt Gutenberg, einschließlich Biographien, Bildern und einer Liste von veröffentlichten Büchern.
   - Scraped die Texte aller Bücher des Autors, um eine Textanalyse zu ermöglichen.

2. **Texteingabe und Autorenerkennung:**
   - Analysiert eingegebene Texte mithilfe eines Naive-Bayes-Modells, um die Wahrscheinlichkeit anzugeben, welchem Autor der Text wahrscheinlich zuzuordnen ist.

3. **Modelltraining:**
   - Verwendet `CountVectorizer` zur Umwandlung von Texten in numerische Features und `MultinomialNB` für die Klassifizierung.
   - Bewertet die Genauigkeit des Modells und zeigt diese in der Benutzeroberfläche an.

## Code Übersicht

- **`gutenberg_main.py`:** Hauptanwendung, die die Benutzeroberfläche und die Interaktion mit dem Scraping-Modul und dem Analyse-Modul bereitstellt.
- **`gutenberg_scraping.py`:** Modul zum Scrapen von Autorendaten und Buchtexten von Projekt Gutenberg.
- **`gutenberg_model.py`:** Modul zur Analyse der gescrapten Texte und zum Training des Klassifikationsmodells.

## Funktionsweise

1. **Streamlit-Anwendung:** Die Benutzeroberfläche wird mit Streamlit erstellt und bietet die Möglichkeit, Autoreninformationen zu scrapen und Textanalysen durchzuführen.
2. **Scraping-Funktionen:** Nutzt BeautifulSoup zum Parsen der HTML-Daten von Projekt Gutenberg und extrahiert relevante Informationen und Texte.
3. **Textanalyse:** Die gescrapten Texte werden in ein Modell integriert, das auf Basis von `CountVectorizer` und `MultinomialNB` trainiert wird.

## Contributing

Beiträge zum Projekt sind willkommen! Bitte erstelle einen Pull-Request mit deinen Änderungen oder Vorschlägen.

