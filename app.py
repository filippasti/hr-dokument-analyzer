import streamlit as st
from pypdf import PdfReader
import anthropic
from dotenv import load_dotenv
import os

# ─── Setup ──────────────────────────────────────────────────────────────
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.set_page_config(
    page_title="HR-Dokument-Analyzer",
    page_icon="📄",
    layout="centered"
)

# Chat-Verlauf initialisieren
if "chat_verlauf" not in st.session_state:
    st.session_state.chat_verlauf = []

# ─── Hilfsfunktion ──────────────────────────────────────────────────────
def pdf_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ─── Kopfbereich ────────────────────────────────────────────────────────
st.title("📄 HR-Dokument-Analyzer")
st.caption("KI-gestützte Analyse von Lebensläufen und Stellenausschreibungen – powered by Claude")
st.divider()

# ─── Tabs ───────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Einzelanalyse", "Matching", "Chat"])

# ═══ TAB 1: Einzelanalyse ═══════════════════════════════════════════════
with tab1:
    st.subheader("Dokument analysieren")
    st.write("Lade ein PDF hoch und wähle, welche Analyse Claude durchführen soll.")

    uploaded_file = st.file_uploader("PDF auswählen", type="pdf", key="single")

    if uploaded_file is not None:
        st.success(f"{uploaded_file.name} geladen")
        text = pdf_to_text(uploaded_file)

        with st.expander("Eingelesenen Text anzeigen"):
            st.text_area("Inhalt", text, height=200, label_visibility="collapsed")

        analyse_typ = st.selectbox("Analyse-Typ",
            ["Zusammenfassung", "Skills extrahieren", "Stärken & Schwächen"])

        if st.button("Analysieren", key="btn_single", type="primary"):
            prompt = f"""Führe folgende Analyse durch: {analyse_typ}

Ignoriere Kopf- und Fußzeilen. Hier ist das HR-Dokument:

{text}"""

            with st.spinner("Claude analysiert das Dokument..."):
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )

            st.divider()
            st.subheader("Ergebnis")
            st.markdown(message.content[0].text)

# ═══ TAB 2: Matching ════════════════════════════════════════════════════
with tab2:
    st.subheader("Lebenslauf und Stelle abgleichen")
    st.write("Lade beide Dokumente hoch und erhalte eine prozentuale Passung mit Gap-Analyse.")

    col1, col2 = st.columns(2)
    with col1:
        cv_file = st.file_uploader("Lebenslauf", type="pdf", key="cv")
    with col2:
        job_file = st.file_uploader("Stellenausschreibung", type="pdf", key="job")

    if cv_file is not None and job_file is not None:
        cv_text = pdf_to_text(cv_file)
        job_text = pdf_to_text(job_file)
        st.success("Beide Dokumente geladen")

        if st.button("Matching starten", key="btn_match", type="primary"):
            prompt = f"""Du bist ein erfahrener HR-Experte. Vergleiche den folgenden 
Lebenslauf mit der Stellenausschreibung. Strukturiere deine Antwort klar mit Überschriften:

## Match-Bewertung
Gib eine Passung in Prozent an.

## Erfüllte Anforderungen
Welche Anforderungen erfüllt der Kandidat?

## Lücken
Welche Anforderungen fehlen oder sind schwach?

## Empfehlung
Eine kurze Handlungsempfehlung.

STELLENAUSSCHREIBUNG:
{job_text}

LEBENSLAUF:
{cv_text}"""

            with st.spinner("Claude vergleicht die Dokumente..."):
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                )

            st.divider()
            st.markdown(message.content[0].text)
    else:
        st.info("Bitte lade beide Dokumente hoch, um das Matching zu starten.")

# ═══ TAB 3: Chat ════════════════════════════════════════════════════════
with tab3:
    st.subheader("Mit Claude chatten")

    if st.session_state.chat_verlauf:
        if st.button("Verlauf löschen", key="btn_clear"):
            st.session_state.chat_verlauf = []
            st.rerun()

    for nachricht in st.session_state.chat_verlauf:
        with st.chat_message(nachricht["role"]):
            st.markdown(nachricht["content"])

    if prompt := st.chat_input("Frag mich etwas..."):
        st.session_state.chat_verlauf.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Claude denkt nach..."):
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    messages=st.session_state.chat_verlauf
                )
                antwort = message.content[0].text
                st.markdown(antwort)

        st.session_state.chat_verlauf.append({"role": "assistant", "content": antwort})