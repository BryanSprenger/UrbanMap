import streamlit as st

st.set_page_config(page_title="Editor OSM Local", layout="wide")

st.title("🗺️ Editor OSM - Versão Simples")

with open("UrbanMap/id_editor.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=700, scrolling=True)
