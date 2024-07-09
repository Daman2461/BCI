import os
import json
import threading
import pygame
from dotenv import load_dotenv
from websocket import create_connection

# Load environment variables from .env file
load_dotenv()

clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

# Shared variables
ws = None
cortexToken = None
action_data = None
action_data_lock = threading.Lock()

def connect_to_emotiv():
    global ws, cortexToken
    # Establish WebSocket connection to Emotiv API
    ws = create_connection("wss://localhost:6868")

    # Load Cortex Token from file or secure storage
    with open("cortex_token.txt", "r") as file:
        cortexToken = file.read().strip()

def send_message(j):
    j = json.dumps(j)
    ws.send(j)
    response = ws.recv()
    return json.loads(response)

def handle_emotiv_data():
    global action_data
    try:
        # Create a session with the headset
        response = send_message({
            "id": 1,
            "jsonrpc": "2.0",
            "method": "createSession",
            "params": {
                "cortexToken": cortexToken,
                "headset": "EPOCX-E5020513",
                "status": "open"
            }
        })

        sessionId = response['id']
        print("Session created with ID:", sessionId)

        # Load profile
        send_message({
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

        print("Profile loaded")

        while True:
            result = json.loads(ws.recv())
            print("Received data:", result)
            if "com" in result:
                action = result["com"][0]
                power = result["com"][1]

                print("Action:", action, "Power:", power)

                if action == "lift" and power >= 0.3:
                    print("Received lift action with power:", power)
                    with action_data_lock:
                        action_data = {"action": "lift", "power": power}

    except KeyError as e:
        print(f"KeyError: {str(e)}")
        print("Response:", response)
        print("Unable to retrieve session ID. Check API response structure.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("An error occurred during API interaction.")
    finally:
        ws.close()

def game_loop():
    global action_data
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("BCI Controlled Game")

    # Game variables
    box_y = 300  # Initial position of the box

    # Game loop
    running = True
    clock = pygame.time.Clock()  # Initialize Pygame clock for frame rate control
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            # Process action data received from Emotiv
            with action_data_lock:
                if action_data:
                    print("Action data:", action_data)
                    if action_data["action"] == "lift" and action_data["power"] >= 0.3:
                        print(f"Lift action detected with power: {action_data['power']}")
                        # Adjust box position based on BCI input
                        box_y = 100

            # Clear the screen
            screen.fill((255, 255, 255))

            # Draw the box based on its current position
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(400, box_y, 50, 50))

            # Update Pygame display
            pygame.display.flip()

        except Exception as e:
            print(f"Error during game loop: {e}")

        # Cap the frame rate to 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    connect_to_emotiv()

    # Start the Emotiv data handling thread
    emotiv_thread = threading.Thread(target=handle_emotiv_data)
    emotiv_thread.start()

    # Start the game loop
    game_loop()

    # Wait for the Emotiv thread to finish
    emotiv_thread.join()
