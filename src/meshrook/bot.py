
import asyncio
import logging
from datetime import datetime

from meshcore import MeshCore, EventType

ADDRESS = ""

logging.basicConfig(level=logging.ERROR)
class ContactDebugFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return any(s in msg for s in (
            "Getting contacts",
            "Received data:",
            "no event received",
        ))

debug_filter = ContactDebugFilter()
mesh_logger = logging.getLogger("meshcore")
#mesh_logger.setLevel(logging.DEBUG)
#mesh_logger.addFilter(debug_filter)

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
#    result = await mesh.commands.get_contacts()
    from meshcore import EventType

    received = asyncio.Event()

    async def on_contacts(event):
        print("ODEBRANO CONTACTS:", len(event.payload or {}))
        print("Atrybuty:", event.attributes)
        received.set()

    mesh.subscribe(EventType.CONTACTS, on_contacts)

    await mesh.commands.get_contacts_async()

    try:
        await asyncio.wait_for(received.wait(), timeout=5)
    except asyncio.TimeoutError:
        print("Brak CONTACTS w ciągu 5 sekund")

    print("Liczba kontaktów w mesh.contacts:", len(mesh.contacts))
#---
#    print("Wynik pobierania kontaktów:", repr(result))
    print("Liczba kontaktów:", len(mesh.contacts))
#    print("Kontakty:", repr(mesh.contacts))

    async def on_message(event):
        msg = event.payload or {}
        #now = datetime.now().astimezone().isoformat(timespec="seconds")
        now = datetime.now().astimezone().strftime("%H:%M:%S%z")[:-2]

        sender = msg.get("pubkey_prefix", "")
        contact = mesh.get_contact_by_key_prefix(sender)

        print("Kontakt znaleziony:", repr(contact))

        contacts = getattr(mesh, "contacts", None)
#        print("Typ mesh.contacts:", type(contacts).__name__)
#        print("mesh.contacts:", repr(contacts))
        print("Kontakt nadawcy:", repr(contact))
        print("Połączenie aktywne:", mesh.is_connected)


        text = msg.get("text", "")

        # Pełny zapis tego, co faktycznie udostępniła biblioteka.
        print(f"\n[{now}] CONTACT_MSG_RECV")
        print(f"payload: {msg!r}")
        print(f"attributes: {event.attributes!r}")

        if not sender:
            print("Brak pubkey_prefix — nie można ustalić adresata odpowiedzi.")
            return

        # Użyj kontaktu, jeśli jest w lokalnej bazie.
        # W przeciwnym razie spróbuj użyć prefiksu klucza.
        contact = mesh.get_contact_by_key_prefix(sender)
        print("Kontakt znaleziony:", repr(contact))
        destination = contact if contact is not None else sender
        name = contact.get("adv_name") if contact and contact.get("adv_name") else sender
        #time_short = now.strftime("%H:%M:%S%z")[:-2]
        time_short = now
        report = (
            "Raport odbioru wiadomości\n"
            f"Czas: {now}\n"
            f"Nadawca: {sender}\n"
            f"Treść: {text}\n"
            f"Payload: {msg!r}\n"
            f"Atrybuty zdarzenia: {event.attributes!r}"
        )
        report = f"@[{name}] time:{time_short}"
        try:
            result = await mesh.commands.send_msg(destination, report)
            print("WYNIK send_msg:", repr(result))
            print("TYP wyniku:", result.type)
            print("PAYLOAD wyniku:", repr(result.payload))
            if result.is_error():
                print(f"Błąd wysyłania raportu: {result.payload!r}")
            else:
                print(f"Wysłano raport do {sender}; wynik: {result.payload!r}")
        except Exception as exc:
            print(f"Wyjątek przy wysyłaniu raportu: {exc!r}")

    async def on_disconnect(event):
        print(f"Utracono połączenie: {event.payload}")


    async def on_msg_sent(event):
        print("MSG_SENT:", repr(event.payload), repr(event.attributes))

    async def on_error(event):
        print("ERROR:", repr(event.payload), repr(event.attributes))

#-- temp
    async def on_msg_sent(event):
        print("MSG_SENT:", repr(event.payload))

    async def on_error(event):
        print("ERROR:", repr(event.payload))

    async def on_ok(event):
        print("OK:", repr(event.payload))

    mesh.subscribe(EventType.MSG_SENT, on_msg_sent)
    mesh.subscribe(EventType.ERROR, on_error)
    mesh.subscribe(EventType.OK, on_ok)

#-- end temp
    mesh.subscribe(EventType.CONTACT_MSG_RECV, on_message)
    mesh.subscribe(EventType.DISCONNECTED, on_disconnect)
    mesh.subscribe(EventType.MSG_SENT, on_msg_sent)
    mesh.subscribe(EventType.ERROR, on_error)


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
