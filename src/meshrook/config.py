"""Konfiguracja bota.

Wartości ustawia load(), wołane raz w app.main() po sparsowaniu argumentów.
Reszta kodu importuje moduł (from meshrook import config) i czyta
config.NAZWA w momencie użycia.

Nie importować wartości bezpośrednio (from meshrook.config import ADDRESS)
i nie używać ich jako domyślnych argumentów funkcji, bo wtedy zostaną
skopiowane przed wczytaniem pliku.
"""

import os
import tomllib
from pathlib import Path

# Wartości przed wczytaniem pliku. Opcjonalne ustawienia z wartością
# domyślną dopisujemy w load() przez data.get(...).
ADDRESS: str | None = None


def _find_config_path(explicit: Path | None) -> Path:
    """Wskazany plik albo pierwszy istniejący z domyślnych lokalizacji."""
    if explicit is not None:
        # Jawna ścieżka: brak pliku to błąd, bez cichego fallbacku.
        if not explicit.is_file():
            raise FileNotFoundError(f"Nie znaleziono pliku konfiguracji: {explicit}")
        return explicit

    xdg = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    candidates = [
        Path("config.toml"),
        xdg / "meshrook" / "config.toml",
        ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Nie znaleziono config.toml. Szukano w: "
        + ", ".join(str(c) for c in candidates)
    )


def load(path: Path | None = None) -> Path:
    """Wczytuje konfigurację i ustawia wartości w tym module.

    Zwraca ścieżkę użytego pliku.
    """
    global ADDRESS

    config_path = _find_config_path(path)
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    try:
        ADDRESS = data["companion"]["address"]
    except KeyError as exc:
        raise ValueError(f"{config_path}: brak wymaganego pola [companion] address") from exc

    return config_path


if __name__ == "__main__":
    # used = load(Path("C:/Users/chris/IdeaProjects/mesh-rook/config.toml"))
    used = load()
    print("Plik:", used)
    print("ADDRESS =", ADDRESS)
