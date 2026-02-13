import asyncio
import websockets
import paho.mqtt.client as mqtt
import json

TEAM_ID = "team05"
MQTT_TOPIC = f"vision/{TEAM_ID}/movement"
MQTT_BROKER = "localhost"

connected_clients = set()

# ===== MQTT callback =====
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    # schedule broadcast in the running loop
    asyncio.run_coroutine_threadsafe(broadcast(data), loop)

async def broadcast(message):
    for ws in connected_clients.copy():
        try:
            await ws.send(message)
        except:
            connected_clients.remove(ws)

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

# ===== MQTT setup =====
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

# ===== Asyncio server =====
async def main():
    async with websockets.serve(handler, "0.0.0.0", 9002):
        print("WebSocket server running on ws://0.0.0.0:9002")
        await asyncio.Future()  # run forever

# ===== Run on Windows =====
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
