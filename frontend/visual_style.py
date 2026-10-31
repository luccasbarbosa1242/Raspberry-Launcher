"""Local presentation-only visual styles.

No database writes, no cloud access, no changes to the application controller.
The existing dark/light/system preference stays under the backend's control.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_STYLE = "raspberry_neon"
PROVISIONAL_FIGMA_STYLE = "figma_preview"
STYLES = {
    DEFAULT_STYLE: ("Raspberry Neon", "Design roxo/magenta aprovado"),
    PROVISIONAL_FIGMA_STYLE: ("Figma (prévia)", "Estilo temporário: protótipo ainda não lido"),
    "sapphire": ("Azul Safira", "Azul elétrico + ciano • moderno"),
    "emerald": ("Verde Esmeralda", "Verde + menta • natural"),
    "ruby": ("Vermelho Rubi", "Vermelho + bordô • intenso"),
    "sunset": ("Pôr do Sol", "Coral + âmbar • acolhedor"),
    "imperial_gold": ("Dourado Imperial", "Ouro + bronze • elegante"),
    "sakura": ("Rosa Sakura", "Rosa + lavanda • delicado"),
    "galaxy": ("Galáxia", "Índigo + azul • espacial"),
    "graphite": ("Grafite", "Cinza + prata • minimalista"),
}


def settings_file() -> Path:
    """Write only to the user's own UI preferences, never DATA/library.db."""
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    return base / "RaspberryLC" / "visual_themes.json"


def _read() -> dict:
    try:
        data = json.loads(settings_file().read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (OSError, ValueError, TypeError):
        pass
    return {}


def load_style(profile_id: str | None = None) -> str:
    data = _read()
    profiles = data.get("profiles", {})
    chosen = profiles.get(profile_id) if profile_id and isinstance(profiles, dict) else None
    if chosen not in STYLES:
        chosen = data.get("last_style", DEFAULT_STYLE)
    return chosen if chosen in STYLES else DEFAULT_STYLE


def save_style(style: str, profile_id: str | None = None) -> bool:
    if style not in STYLES:
        raise ValueError("Estilo visual inválido")
    data = _read()
    profiles = data.get("profiles", {})
    if not isinstance(profiles, dict):
        profiles = {}
    if profile_id:
        profiles[str(profile_id)] = style
    data = {"version": 1, "last_style": style, "profiles": profiles}
    path = settings_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp_path, path)
        return True
    except OSError:
        return False
