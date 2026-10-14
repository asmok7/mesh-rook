
import asyncio
import logging
from datetime import datetime

from meshcore import MeshCore, EventType

ADDRESS = "10:BD:A3:5B:A1:51"

logging.basicConfig(level=logging.WARNING)


async def main():
    mesh = await MeshCore.create_ble(
        address=ADDRESS,
        auto_reconnect=True,
        debug=False,
    )

    if mesh is None:
        print("Nie udało się połączyć z Companionem.")
        return

    print(f"Połączono z {mesh.self_info.get('name', 'Companion')}")

    async def on_message(event):
        msg = event.payload or {}
        now = datetime.now().astimezone().isoformat(timespec="seconds")

        sender = msg.get("pubkey_prefix", "nieznany")
        text = msg.get("text", "")

        print(f"[{now}] Wiadomość od {sender}: {text}")

    async def on_disconnect(event):
        print(f"Utracono połączenie: {event.payload}")

    mesh.subscribe(EventType.CONTACT_MSG_RECV, on_message)
    mesh.subscribe(EventType.DISCONNECTED, on_disconnect)

    await mesh.start_auto_message_fetching()

    print("Nasłuchuję wiadomości prywatnych. Ctrl+C kończy pracę.")

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await mesh.stop_auto_message_fetching()
        await mesh.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nZatrzymano bota.")
