import streamlit as st
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Editor OSM Local", layout="wide")

st.title("🧭 Editor de Desenho OSM (iD) - Versão Básica com Verificação")

st.markdown("""
Essa versão tenta carregar o editor **iD (OpenStreetMap)** e exibe uma mensagem caso o carregamento falhe.
""")

# Caminho do HTML
html_path = os.path.join("static", "id_editor.html")

# Lê o arquivo
try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("❌ O arquivo `id_editor.html` não foi encontrado na pasta `static/`.")
    st.stop()

# Adiciona script de verificação de carregamento
html_with_check = f"""
{html_code}
<script>
window.addEventListener('error', function(event) {{
    const message = "Erro ao carregar o editor iD: " + (event.message || "falha desconhecida");
    window.parent.postMessage({{ type: 'osm_error', message: message }}, '*');
}});
window.addEventListener('load', function() {{
    window.parent.postMessage({{ type: 'osm_loaded' }}, '*');
}});
</script>
"""

# Exibe o editor e adiciona um canal de comunicação com o Streamlit
components.html(f"""
<html>
<head><meta charset="utf-8"></head>
<body>
    <div id="osm-container"></div>
    <script>
        // Recebe mensagens do iframe interno (iD editor)
        window.addEventListener('message', (event) => {{
            if (event.data?.type === 'osm_error') {{
                const errorBox = parent.document.querySelector('#osm-error');
                if (errorBox) {{
                    errorBox.innerText = event.data.message;
                    errorBox.style.display = 'block';
                }}
            }}
            if (event.data?.type === 'osm_loaded') {{
                const okBox = parent.document.querySelector('#osm-ok');
                if (okBox) {{
                    okBox.style.display = 'block';
                }}
            }}
        }});
    </script>
    <iframe srcdoc="{html_with_check.replace('"', '&quot;')}" 
            width="100%" height="700" style="border:none;"></iframe>
</body>
</html>
""", height=750)

# Caixas de status no Streamlit
st.markdown("""
<div style="margin-top: 1em;">
  <div id="osm-ok" style="display:none; color:green; font-weight:bold;">
    ✅ Editor carregado com sucesso.
  </div>
  <div id="osm-error" style="display:none; color:red; font-weight:bold;">
    ❌ Erro ao carregar o editor. Verifique sua conexão ou bloqueio de scripts.
  </div>
</div>
""", unsafe_allow_html=True)
