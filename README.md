# IPTV Channels Sync

Scraper en Python que accede a páginas oficiales de emisión en directo de canales de TV españoles, intenta extraer la primera URL de stream con extensión `.m3u8` y genera un fichero `streams.m3u`.

Si se proporcionan credenciales por variables de entorno, el script también actualiza automáticamente `streams.m3u` en este repositorio usando la API de GitHub.

## Canales soportados

- RTVE La 1
- Antena 3
- Telecinco
- La Sexta
- Cuatro

## Ejecución local

1. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el scraper:

   ```bash
   python main.py
   ```

3. (Opcional) Para actualizar `streams.m3u` en GitHub al ejecutar localmente, definir variables de entorno:

   - `GITHUB_TOKEN`
   - `GITHUB_REPO` (formato: `usuario/repositorio`)

## Workflow de GitHub Actions

El workflow `.github/workflows/update_streams.yml`:

- Se ejecuta automáticamente cada 6 horas
- Puede ejecutarse manualmente desde la pestaña **Actions**
- Instala dependencias y lanza `python main.py`
- Usa:
  - `GITHUB_TOKEN` (de `secrets.GITHUB_TOKEN`)
  - `GITHUB_REPO` (de `github.repository`)

## Variables de entorno necesarias

- `GITHUB_TOKEN`: token para autenticar contra la API de GitHub.
- `GITHUB_REPO`: repositorio objetivo en formato `usuario/repo`.

## Uso responsable

Este proyecto debe usarse de forma responsable y respetando los términos de servicio (TOS), restricciones técnicas y condiciones legales de cada cadena/plataforma.
