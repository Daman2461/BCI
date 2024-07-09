import os
from dotenv import load_dotenv
from websocket import create_connection, WebSocket
import json
import threading
import asyncio
import websockets

load_dotenv()

clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
print("clientId: ", clientId)
print("clientSecret: ", clientSecret)

# WebSocket connection to Emotiv Cortex
ws = create_connection("wss://localhost:6868")
def send_message(j):
    j = json.dumps(j)
    ws.send(j)
    response = ws.recv()
    return response

# Request access to Cortex
getCortexToken = send_message({
    "id": 3,
    "jsonrpc": "2.0",
    "method": "requestAccess",
    "params": {
        "clientId": clientId,
        "clientSecret": clientSecret
    }
})

getCortexToken = send_message({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "authorize",
    "params": {
        "clientId": clientId,
        "clientSecret": clientSecret
    }
})

getCortexToken = json.loads(getCortexToken)
cortexToken = getCortexToken["result"]["cortexToken"]

# Create session
createSession = send_message({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "createSession",
    "params": {
        "cortexToken": cortexToken,
        "headset": "EPOCX-E5020513",
        "status": "open"
    }
})

createSession = json.loads(createSession)

try:
    sessionId = createSession['result']['id']
except Exception as e:
    print(str(e))
    print("Unable to connect to headset")
    exit(1)

# Load profile
load_profile = send_message({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "setupProfile",
    "params": {
        "cortexToken": cortexToken,
        "headset": "EPOCX-E5020513",
        "profile": "daman2",
        "status": "load"
    }
})

# Subscribe to data streams
subscribe = send_message({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "subscribe",
    "params": {
        "cortexToken": cortexToken,
        "session": sessionId,
        "streams": ["com"]  # Adjust streams as needed
    }
})

subscribe = json.loads(subscribe)
print("Subscription result:", subscribe)

# WebSocket server to send data to game
async def send_to_game(websocket, path):
    print("Game connected")
    while True:
        result = ws.recv()
        result = json.loads(result)
        print(result)

        if "com" in result:
            action = result["com"][0]
            power = result["com"][1]
            print("Action:", action)
            if action == 'lift':
                await websocket.send(json.dumps({"action": action, "power": power}))
                print("Sent action to game:", {"action": action, "power": power})

# Start WebSocket server
async def start_server():
    server = await websockets.serve(send_to_game, "localhost", 8000)
    print("WebSocket server started on ws://localhost:8000")
    await server.wait_closed()

# Run WebSocket server in a separate thread
server_thread = threading.Thread(target=asyncio.run, args=(start_server(),))
server_thread.start()

print("Backend is running and processing data...")

# Main loop to keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    ws.close()
    sys.exit(0)
