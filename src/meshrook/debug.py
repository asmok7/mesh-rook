"""Narzędzia diagnostyczne na czas rozwoju."""

import logging

from meshcore import EventType, MeshCore


class ContactDebugFilter(logging.Filter):
    """Przepuszcza tylko wybrane komunikaty debugowe biblioteki meshcore."""

    def filter(self, record):
        msg = record.getMessage()
        return any(s in msg for s in (
            "Getting contacts",
            "Received data:",
            "no event received",
        ))


def enable_meshcore_debug() -> None:
    """Włącza poziom DEBUG dla biblioteki meshcore (z filtrem)."""
    mesh_logger = logging.getLogger("meshcore")
    mesh_logger.setLevel(logging.DEBUG)
    mesh_logger.addFilter(ContactDebugFilter())


def attach_event_logging(mesh: MeshCore) -> None:
    """Wypisuje zdarzenia MSG_SENT, ERROR i OK. Każde jest subskrybowane raz."""

    async def on_msg_sent(event):
        print("MSG_SENT:", repr(event.payload))

    async def on_error(event):
        print("ERROR:", repr(event.payload))

    async def on_ok(event):
        print("OK:", repr(event.payload))

    mesh.subscribe(EventType.MSG_SENT, on_msg_sent)
    mesh.subscribe(EventType.ERROR, on_error)
    mesh.subscribe(EventType.OK, on_ok)
