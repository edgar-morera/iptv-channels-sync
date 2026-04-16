import os
from github import Github, GithubException
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

PLAY_BUTTON_TIMEOUT_MS = 2_000   # ms to wait for a play button to be visible
STREAM_START_TIMEOUT_MS = 8_000  # ms to wait for the m3u8 request after clicking play

# --- Extracción de URLs m3u8 con Playwright ---
def extract_m3u8_playwright(url: str) -> str | None:
    """Abre la página con Chromium headless, intercepta peticiones de red y
    devuelve la primera URL .m3u8 capturada, o None si no se encuentra."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"Error al cargar {url}: {type(e).__name__}: {e}")
            browser.close()
            return None

        # Intentar pulsar el botón de play si existe
        play_selectors = [
            'button[class*="play"]',
            '[aria-label*="play" i]',
            '.play-button',
            'button[class*="Play"]',
            '[data-testid*="play" i]',
        ]
        for selector in play_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible(timeout=PLAY_BUTTON_TIMEOUT_MS):
                    btn.click()
                    break
            except Exception:
                continue

        # Esperar la primera petición .m3u8 (salir en cuanto llegue)
        stream_url: str | None = None
        try:
            req = page.wait_for_event(
                "request",
                predicate=lambda r: ".m3u8" in r.url,
                timeout=STREAM_START_TIMEOUT_MS,
            )
            stream_url = req.url
        except PlaywrightTimeoutError:
            pass

        browser.close()

    return stream_url

# --- Definición de canales ---
CHANNELS = [
    {"name": "TVE La 1",  "url": "https://www.rtve.es/play/videos/directo/canales-lineales/la-1/"},
    {"name": "TVE La 2",  "url": "https://www.rtve.es/play/videos/directo/canales-lineales/la-2/"},
    {"name": "Antena 3",  "url": "https://www.atresplayer.com/directos/antena3/"},
    {"name": "Cuatro",    "url": "https://www.cuatro.com/en-directo/"},
    {"name": "Telecinco", "url": "https://www.telecinco.es/endirecto/"},
    {"name": "La Sexta",  "url": "https://www.atresplayer.com/directos/lasexta/"},
]

# --- Generación del fichero M3U ---
def build_m3u(results: list[dict]) -> str:
    lines = ["#EXTM3U"]
    for ch in results:
        if ch.get("stream_url"):
            lines.append(f'#EXTINF:-1,{ch["name"]}')
            lines.append(ch["stream_url"])
    return "\n".join(lines)

# --- Subida al repo de GitHub ---
def push_to_github(content: str, token: str, repo_name: str, file_path: str = "streams.m3u"):
    g = Github(token)
    repo = g.get_repo(repo_name)
    try:
        existing = repo.get_contents(file_path)
        repo.update_file(file_path, "🔄 Actualizar streams.m3u", content, existing.sha)
        print(f"Fichero actualizado: {file_path}")
    except GithubException as e:
        if e.status != 404:
            print(f"Error al actualizar {file_path} en GitHub (status {e.status}): {type(e).__name__}: {e}")
            raise
        repo.create_file(file_path, "✨ Crear streams.m3u", content)
        print(f"Fichero creado: {file_path}")

# --- Main ---
if __name__ == "__main__":
    results = []
    for channel in CHANNELS:
        print(f"Procesando: {channel['name']}...")
        stream_url = extract_m3u8_playwright(channel["url"])
        results.append({**channel, "stream_url": stream_url})
        print(f"  → {stream_url or 'No encontrada'}")

    m3u_content = build_m3u(results)
    print("\n--- Contenido generado ---")
    print(m3u_content)

    # Subir a GitHub (requiere GITHUB_TOKEN y GITHUB_REPO como variables de entorno)
    token = os.environ.get("GITHUB_TOKEN")
    repo  = os.environ.get("GITHUB_REPO")  # formato: "usuario/repo"
    if token and repo:
        push_to_github(m3u_content, token, repo)
