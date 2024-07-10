import os
from dotenv import load_dotenv
from websocket import create_connection
import json
from queue import Queue
from threading import Thread
from time import sleep

load_dotenv()

clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
print("clientId: ", clientId)
print("clientSecret: ", clientSecret)

# WebSocket connection with SSL verification disabled
ws = create_connection("wss://localhost:6868", sslopt={"cert_reqs": 0})

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

print("Sent")
print("Receiving...")

# Continuously receive and process data
def process_data(queue):
    while True:
        result = ws.recv()
        result = json.loads(result)
        print(result)

        if "com" in result:
            action = result["com"][0]
            power = result["com"][1]
            print("Action:", action)

            if action == 'lift':
                queue.put('move_up')
            else:
                queue.put('stay')  # Send 'stay' command if action is not 'lift'
            
        sleep(0.1)  # Adjust sleep time as needed
