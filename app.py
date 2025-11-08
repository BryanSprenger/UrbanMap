import streamlit as st
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Editor OSM Local", layout="wide")

st.title("🧭 Editor de Desenho OSM (iD) - Versão Aprimorada")

st.markdown("""
Essa versão aprimorada carrega o editor **iD (OpenStreetMap)** e usa a comunicação JavaScript/Streamlit para exibir o **status de carregamento** de forma limpa.
""")

# --- 1. Inicializa o estado de carregamento ---
if 'osm_status' not in st.session_state:
    st.session_state.osm_status = 'initial' # initial, loading, loaded, error
if 'osm_error_message' not in st.session_state:
    st.session_state.osm_error_message = ''

# --- 2. Carrega o HTML do iD ---
html_path = os.path.join("static", "id_editor.html")

try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("❌ O arquivo `id_editor.html` não foi encontrado na pasta `static/`.")
    st.stop()

# --- 3. Script para Receber Mensagens e Atualizar o Estado (Key Point) ---
# Este script é a chave para comunicar o status do JS de volta para o Python.
# O Streamlit executará este script após o components.html ser renderizado.
js_listener = f"""
<script>
    // Envia o status para o Streamlit (Python)
    function sendMessageToStreamlit(status, message = '') {{
        Streamlit.set
        if (window.parent.streamlitReportMessage) {{
            window.parent.streamlitReportMessage({{
                type: 'streamlit:setComponentValue',
                componentId: 'osm_status_receiver',
                value: {{ status: status, message: message }}
            }});
        }}
    }}

    // Adiciona listener para mensagens vindas do iframe (o conteúdo do editor iD)
    window.addEventListener('message', (event) => {{
        // Verifica a origem se for necessário, por simplicidade estamos usando '*'
        if (event.data && event.data.type === 'osm_status') {{
            const status = event.data.status;
            const message = event.data.message || '';
            
            // Aqui, enviamos os dados de volta para o Streamlit (o componente)
            // No entanto, como estamos usando components.html puro, a comunicação
            // direta de volta para o Python sem um componente customizado é mais complexa.
            // A solução mais robusta é usar o truque do 'setComponentValue' com um componente 'dummy'
            // ou, simplificando, enviar os dados para um endpoint, mas o Streamlit não tem isso.

            // Simplificando o fluxo: vamos depender do status que o JS envia ao parent (que é o Streamlit)
            // e atualizar o estado da sessão na próxima execução do script Python (re-run).
            
            // Para *simplicidade e demonstração* (pois components.html não tem um canal de retorno fácil),
            // simulamos uma comunicação enviando o status de volta:
            const data = {{ status: status, message: message }};
            // Usaremos um truque: o Streamlit não aceita setComponentValue em components.html simples.
            // Para fazer a comunicação de volta, precisamos de um componente customizado real
            // ou usar um elemento que o Streamlit possa inspecionar (o que é inviável).
            
            // A forma mais direta *dentro do components.html* é a que movemos para o HTML do iD
            // (a lógica 'window.parent.postMessage').
            
            // Para *exibir* o status no Streamlit (o Python), faremos uma abordagem visual:
            const statusBox = parent.document.getElementById('osm-status-box');
            if (statusBox) {{
                statusBox.innerText = status.toUpperCase() + (message ? ' - ' + message : '');
                if (status === 'loaded') {{
                    statusBox.style.color = 'green';
                }} else if (status === 'error') {{
                    statusBox.style.color = 'red';
                }} else {{
                    statusBox.style.color = 'orange';
                }}
            }}
        }}
    }});
</script>
"""

# --- 4. Exibe o Editor iD e o Status Box ---
# Colocamos a lógica de recebimento do JS DENTRO do components.html, pois ele é o parent do editor iD.
full_html_with_listener = f"""
<html>
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 0; height: 100%;">
    <div id="osm-status-box" style="padding: 5px; color: orange; font-weight: bold;">
        Carregando...
    </div>

    <iframe srcdoc="{html_code.replace('"', '&quot;')}" 
            width="100%" height="700" style="border:none; display:block;"></iframe>

    {js_listener}
</body>
</html>
"""

components.html(full_html_with_listener, height=750, scrolling=False)

# --- 5. Feedback Visual no Streamlit (Abaixo do iframe) ---

# Em componentes.html simples, o canal de comunicação de volta para o Python (st.session_state) 
# é muito limitado. A solução mais prática é usar um feedback visual *dentro* do próprio HTML do iframe
# (como feito com o #osm-status-box) e complementar com um status inicial no Python.

st.markdown("---")

if st.session_state.osm_status == 'initial':
    st.info("ℹ️ O editor iD está sendo carregado. O status será exibido acima.")
elif st.session_state.osm_status == 'loaded':
    st.success("✅ Editor carregado com sucesso!")
elif st.session_state.osm_status == 'error':
    st.error(f"❌ Erro de carregamento: {st.session_state.osm_error_message} (Verifique o console do navegador).")

st.markdown("""
> **Nota de Implementação:** Devido às limitações de segurança e comunicação do Streamlit com `components.html` simples, o **status em tempo real é atualizado diretamente dentro do iframe** usando o `div id="osm-status-box"`. O Streamlit (código Python) exibe apenas um status inicial ou o último status conhecido antes de um *re-run*.
""")
