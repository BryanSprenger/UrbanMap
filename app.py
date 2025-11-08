import streamlit as st
import streamlit.components.v1 as components

# Configurações do mapa: Centro em Curitiba, Brasil
LAT = -25.43
LON = -49.27
ZOOM = 16

# URL para o editor iD/RapiD, usando o parâmetro embed=true
# Substituímos por uma URL pública que carrega o editor iD
# A URL padrão do OSM iD é: https://www.openstreetmap.org/edit?editor=id#map={ZOOM}/{LAT}/{LON}
# O RapiD (que é o iD melhorado) é um bom substituto para embedding.

# Usaremos um link público do OSM que já inicia o editor iD
osm_editor_url = f"https://www.openstreetmap.org/edit?editor=id#map={ZOOM}/{LAT}/{LON}"

st.title("🗺️ Editor iD Integrado (Link Externo)")
st.info(f"O editor iD será carregado na área com foco em: **{LAT}, {LON}**")

# Use st.components.v1.iframe para carregar a URL pública
# A altura é crucial para visualização
components.iframe(
    src=osm_editor_url, 
    width=1000, 
    height=750, 
    scrolling=True
)

st.markdown("""
> **Observação:** O editor iD padrão do OpenStreetMap pode bloquear o carregamento em `iframe` devido às políticas de segurança (`X-Frame-Options`). Se não carregar, não há como contornar isso a partir do Streamlit. A única forma é usar um serviço que permita explicitamente o embedding.
""")
