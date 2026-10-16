"""Składanie całości: argumenty, konfiguracja, połączenie, pętla główna."""

import argparse
import asyncio
import logging
from pathlib import Path

from meshcore import EventType

from meshrook import config
from meshrook.contacts import refresh_contacts
from meshrook.debug import attach_event_logging  # , enable_meshcore_debug
from meshrook.handlers import make_private_message_handler, on_disconnect
from meshrook.transport import ble


async def run() -> None:
    print(f"Connecting to {config.ADDRESS}...")
    mesh = await ble.connect(config.ADDRESS)
    if mesh is None:
        print("Nie udało się połączyć z Companionem.")
        return

    print(f"Połączono z {mesh.self_info.get('name', 'Companion')}")

    await refresh_contacts(mesh)

    attach_event_logging(mesh)
    mesh.subscribe(EventType.CONTACT_MSG_RECV, make_private_message_handler(mesh))
    mesh.subscribe(EventType.DISCONNECTED, on_disconnect)

    await mesh.start_auto_message_fetching()
    print("Nasłuchuję wiadomości prywatnych. Ctrl+C kończy pracę.")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await mesh.stop_auto_message_fetching()
        await mesh.disconnect()


def main() -> None:
    """Punkt wejścia (python -m meshrook oraz entry point w pyproject.toml)."""
    parser = argparse.ArgumentParser(prog="meshrook", description="MeshRook - bot MeshCore")
    parser.add_argument(
        "--config",
        type=Path,
        metavar="PLIK",
        help="ścieżka do config.toml (domyślnie ./config.toml, potem ~/.config/meshrook/config.toml)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.ERROR)
    # enable_meshcore_debug()

    try:
        used = config.load(args.config)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(f"Błąd konfiguracji: {exc}")
    print(f"Konfiguracja: {used}")

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nZatrzymano bota.")


if __name__ == "__main__":
    main()
