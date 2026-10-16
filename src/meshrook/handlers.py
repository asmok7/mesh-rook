"""Handlery zdarzeń z MeshCore.

Docelowo handler wiadomości prywatnych przekaże tekst do dispatchera poleceń,
a tu zostanie tylko odbiór zdarzenia i wysłanie odpowiedzi.
"""

from datetime import datetime

from meshcore import MeshCore


def make_private_message_handler(mesh: MeshCore):
    """Zwraca handler wiadomości prywatnych związany z danym połączeniem."""

    async def on_private_message(event):
        msg = event.payload or {}
        now = datetime.now().astimezone().strftime("%H:%M:%S%z")[:-2]

        print(f"\n[{now}] CONTACT_MSG_RECV")
        print(f"payload: {msg!r}")
        print(f"attributes: {event.attributes!r}")
        print("Połączenie aktywne:", mesh.is_connected)

        sender = msg.get("pubkey_prefix", "")
        if not sender:
            print("Brak pubkey_prefix, nie można ustalić adresata odpowiedzi.")
            return

        # Kontakt z lokalnej bazy, a jeśli go nie ma, to sam prefiks klucza.
        contact = mesh.get_contact_by_key_prefix(sender)
        print("Kontakt nadawcy:", repr(contact))

        destination = contact if contact is not None else sender
        name = contact.get("adv_name") if contact and contact.get("adv_name") else sender

        report = f"@[{name}] time:{now}"
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

    return on_private_message


async def on_disconnect(event):
    print(f"Utracono połączenie: {event.payload}")
