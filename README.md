# HR-Dokument-Analyzer

Eine KI-gestützte Web-App zur Analyse von HR-Dokumenten, gebaut mit Streamlit und 
der Anthropic Claude API. Das Tool zeigt, wie sich typische HR-Aufgaben – von der 
Dokumentenanalyse bis zum Bewerber-Matching – mit modernen KI-Methoden automatisieren lassen.

## Features

Die App bietet drei Funktionen, übersichtlich in Tabs organisiert:

**📑 Einzelanalyse**  
Lade ein PDF (z. B. einen Lebenslauf) hoch und lass es von Claude analysieren – 
wahlweise als Zusammenfassung, Skill-Extraktion oder Stärken-/Schwächen-Analyse.

**🎯 Matching**  
Lade einen Lebenslauf und eine Stellenausschreibung hoch. Claude vergleicht beide 
und liefert eine prozentuale Passung, eine Auflistung erfüllter und fehlender 
Anforderungen sowie eine Handlungsempfehlung – genau wie beim KI-gestützten Recruiting.

**💬 Chat**  
Ein allgemeiner Chat mit Claude, der sich dank Session-Management an den 
Gesprächsverlauf erinnert.

## Was ich dabei gelernt habe

- Eine interaktive Web-App in Python ohne HTML/CSS/JS bauen (Streamlit)
- Text aus PDF-Dateien extrahieren und verarbeiten (pypdf)
- Prompts dynamisch aufbauen, um je nach Nutzerwunsch unterschiedliche Analysen durchzuführen
- Zustand über mehrere Interaktionen hinweg speichern (st.session_state)
- Wiederverwendbare Funktionen schreiben, um Code-Duplikation zu vermeiden
- API-Keys sicher über Umgebungsvariablen verwalten (.env)

## Tech Stack

- Python 3.13
- Streamlit (Web-Oberfläche)
- Anthropic Claude API (claude-sonnet-4-6)
- pypdf (PDF-Verarbeitung)
- python-dotenv (sicheres API-Key-Management)

## Setup

1. Repository klonen
2. Virtuelle Umgebung erstellen: `python3 -m venv venv`
3. Aktivieren: `source venv/bin/activate`
4. Abhängigkeiten installieren: `pip install -r requirements.txt`
5. `.env` Datei erstellen mit: `ANTHROPIC_API_KEY=dein-key`
6. Starten: `streamlit run app.py`

## Hinweis

Dies ist ein Lernprojekt, das im Rahmen meiner Vorbereitung auf ein Praktikum im 
Bereich HR-IT entstanden ist. Es demonstriert den praktischen Einsatz von LLM-APIs 
zur Optimierung von HR-Prozessen.