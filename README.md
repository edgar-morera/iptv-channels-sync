# IPTV Channels Sync

Scraper en Python que accede a las páginas de emisión en directo de los principales canales de TV españoles, extrae automáticamente las URLs de stream `.m3u8` usando **Playwright** (Chromium headless) e interactuando con los botones de play, y genera un fichero `streams.m3u` que se publica en este repositorio.

## Canales soportados

| Canal | URL |
|---|---|
| TVE La 1 | https://www.rtve.es/play/videos/directo/canales-lineales/la-1/ |
| TVE La 2 | https://www.rtve.es/play/videos/directo/canales-lineales/la-2/ |
| Antena 3 | https://www.atresplayer.com/directos/antena3/ |
| Cuatro | https://www.cuatro.com/en-directo/ |
| Telecinco | https://www.telecinco.es/endirecto/ |
| La Sexta | https://www.atresplayer.com/directos/lasexta/ |

## Ejecución local

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   playwright install chromium --with-deps
   ```

2. Ejecutar el scraper:
   ```bash
   python main.py
   ```

3. (Opcional) Para subir `streams.m3u` al repositorio automáticamente, definir variables de entorno:
   - `GITHUB_TOKEN`: token de acceso a GitHub
   - `GITHUB_REPO`: repositorio en formato `usuario/repo`

## GitHub Actions

El workflow `.github/workflows/update_streams.yml` se ejecuta:
- Automáticamente **cada 6 horas**
- Manualmente desde la pestaña **Actions** → *Run workflow*

## ⚠️ Uso responsable

Este proyecto debe usarse de forma responsable respetando los términos de servicio (TOS) y condiciones legales de cada cadena/plataforma.
