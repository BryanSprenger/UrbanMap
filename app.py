<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="utf-8" />
  <title>Editor OSM Local</title>

  <style>
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    #id-container {
      width: 100%;
      height: 100%;
    }
  </style>

  <!-- Importa o editor iD diretamente da CDN -->
  <script src="https://unpkg.com/@openstreetmap/id@2.21.2/dist/iD.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/@openstreetmap/id@2.21.2/dist/iD.css">
</head>

<body>
  <div id="id-container"></div>

  <script>
    // Inicializa o contexto principal do editor iD
    const context = iD.coreContext()
      .assetPath('https://unpkg.com/@openstreetmap/id@2.21.2/dist/')
      .embed(true);

    // Remove autenticação e conexão remota (modo local/offline)
    context.preauth({ server: null });
    context.connection(null);

    // Define o mapa base padrão (Bing Maps)
    context.background().baseLayerSource(
      iD.data.imagery.find(src => src.id === 'Bing')
    );

    // Renderiza o editor dentro do container
    d3.select('#id-container').call(context.ui());
    context.enter(iD.modes.Browse(context));
  </script>
</body>
</html>

