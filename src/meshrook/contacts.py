"""Pobieranie listy kontaktów z companiona."""

import asyncio

from meshcore import EventType, MeshCore


async def refresh_contacts(mesh: MeshCore, timeout: float = 5.0) -> None:
    """Prosi companiona o kontakty i czeka na odpowiedź (maks. timeout sekund)."""
    received = asyncio.Event()

    async def on_contacts(event):
        print("ODEBRANO CONTACTS:", len(event.payload or {}))
        print("Atrybuty:", event.attributes)
        received.set()

    mesh.subscribe(EventType.CONTACTS, on_contacts)

    await mesh.commands.get_contacts_async()

    try:
        await asyncio.wait_for(received.wait(), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Brak CONTACTS w ciągu {timeout:g} sekund")

    print("Liczba kontaktów w mesh.contacts:", len(mesh.contacts))
