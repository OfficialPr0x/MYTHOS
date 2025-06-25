import json
import websockets
import asyncio

async def emit_signal():
    uri = "ws://localhost:8888"
    with open("signal_packet.json") as f:
        signal_packet = json.load(f)
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps(signal_packet))
        print("📡 Signal emitted to mesh")

if __name__ == "__main__":
    asyncio.run(emit_signal())
