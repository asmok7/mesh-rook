"""Transport BLE: połączenie z companionem."""

import asyncio

from meshcore import MeshCore


async def connect(address: str) -> MeshCore | None:
    """Łączy się z companionem przez BLE. Zwraca None, gdy się nie uda."""
    return await MeshCore.create_ble(
        address=address,
        auto_reconnect=True,
        debug=False,
    )


if __name__ == "__main__":
    from meshrook.config import ADDRESS

    async def _test():
        mesh = await connect(ADDRESS)
        if mesh is None:
            print("Nie udało się połączyć z Companionem.")
            return
        print(f"Połączono z {mesh.self_info.get('name', 'Companion')}")
        await mesh.disconnect()

    asyncio.run(_test())
