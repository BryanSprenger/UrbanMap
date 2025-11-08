# Exemplo de uso de streamlit-folium (precisa instalar: pip install streamlit-folium)
import streamlit as st
from streamlit_folium import folium_static
import folium

st.title("🗺️ Mapa OSM com Folium")
st.info("Esta solução permite visualizar e interagir com o mapa, mas não é o editor iD.")

# Cria um mapa Folium
m = folium.Map(location=[-25.43, -49.27], zoom_start=14)

# Adiciona um marcador
folium.Marker([-25.43, -49.27], popup="Curitiba").add_to(m)

# Exibe o mapa no Streamlit
folium_static(m)
