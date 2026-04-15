import os
import re

import requests
from github import Github


# --- Extracción de URLs m3u8 ---
def extract_m3u8(url: str, headers: dict = None) -> str | None:
    """Accede a una URL y busca la primera URL m3u8 en el HTML/JS."""
    try:
        resp = requests.get(
            url,
            headers=headers or {"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        resp.raise_for_status()
        match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', resp.text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return None


# --- Definición de canales ---
CHANNELS = [
    {"name": "RTVE La 1", "url": "https://www.rtve.es/play/television/directo/la-1/"},
    {"name": "Antena 3", "url": "https://www.antena3.com/directo/"},
    {"name": "Telecinco", "url": "https://www.telecinco.es/directo/"},
    {"name": "La Sexta", "url": "https://www.lasexta.com/directo/"},
    {"name": "Cuatro", "url": "https://www.cuatro.com/directo/"},
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
    except Exception:
        repo.create_file(file_path, "✨ Crear streams.m3u", content)
        print(f"Fichero creado: {file_path}")


# --- Main ---
if __name__ == "__main__":
    results = []
    for channel in CHANNELS:
        print(f"Procesando: {channel['name']}...")
        stream_url = extract_m3u8(channel["url"])
        results.append({**channel, "stream_url": stream_url})
        print(f"  → {stream_url or 'No encontrada'}")

    m3u_content = build_m3u(results)
    print("\n--- Contenido generado ---")
    print(m3u_content)

    # Subir a GitHub (requiere GITHUB_TOKEN y GITHUB_REPO como variables de entorno)
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")  # formato: "usuario/repo"
    if token and repo:
        push_to_github(m3u_content, token, repo)
