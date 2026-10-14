import asyncio
from meshcore import MeshCore
import logging
logging.basicConfig(level=logging.ERROR)


#ADDRESS = "10:BD:A3:5B:0A:2D"
ADDRESS = "10:BD:A3:5B:A1:51"


async def main():
    mesh = await MeshCore.create_ble(
        address=ADDRESS,
        debug=True,
    )

    print("Łączenie...")
    await mesh.connect()
    print("Połączono!")
    
    print("self_info:")
    print(mesh.self_info)

    print("Rozłączanie...")
    await mesh.disconnect()


asyncio.run(main())
