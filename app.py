import streamlit as st

st.set_page_config(page_title="Editor de Desenho OSM", layout="wide")

st.title("🧭 Editor de Desenho OSM (iD) - Versão Básica")

st.markdown("""
Esta versão carrega apenas o editor de desenho do OpenStreetMap, sem conexão ao servidor nem camadas adicionais.
""")

html_code = """
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="utf-8" />
  <title>Editor OSM Local</title>
  <style>
    html, body { height: 100%; margin: 0; }
    #id-container { width: 100%; height: 100%; }
  </style>
  <!-- Biblioteca iD (versão estável) -->
  <script src="https://unpkg.com/@openstreetmap/id@2.21.2/dist/iD.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/@openstreetmap/id@2.21.2/dist/iD.css">
</head>
<body>
  <div id="id-container"></div>
  <script>
    // Cria o contexto principal do iD
    const context = iD.coreContext()
      .assetPath('https://unpkg.com/@openstreetmap/id@2.21.2/dist/')
      .embed(true);

    // Desativa conexão com o servidor OSM
    context.preauth({ server: null });
    context.connection(null);

    // Define o fundo padrão (Bing ou OSM)
    context.background().baseLayerSource(
      iD.data.imagery.find(src => src.id === 'Bing')
    );

    // Renderiza o editor dentro do container
    d3.select('#id-container').call(context.ui());
    context.enter(iD.modes.Browse(context));
  </script>
</body>
</html>
"""

# Exibe o editor
st.components.v1.html(html_code, height=700, scrolling=True)
