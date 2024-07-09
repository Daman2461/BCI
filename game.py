import os
import json
import time
import pygame
from threading import Thread
from websocket import create_connection

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("BCI Controlled Game")

# Game variables
box_y = 300  # Initial position of the box

# WebSocket connection
try:
    ws = create_connection("wss://localhost:8000")
    print("WebSocket connection established.")
except Exception as e:
    print(f"Error connecting to WebSocket: {e}")
     # Exit if WebSocket connection fails

def read_emotiv_data():
    while True:
        try:
            result = ws.recv()
            action_data = json.loads(result)
            print(f"Received action data: {action_data}")  # Print received action data

            # Process action data as needed (adjust box position, trigger game events, etc.)
        
            action = action_data["action"]
            power = action_data["power"]
            print(f"Action: {action}, Power: {power}")  # Print detected action and power

                # Adjust box position based on BCI input
            if action == "lift" and power >= 0.1:
                update_game_state(action, power)  # Update game state based on BCI input

        except Exception as e:
            print(f"Error receiving or decoding WebSocket data: {e}")

def update_game_state(action, power):
    global box_y
    # Example adjustment, modify as needed based on power levels
    if action == "lift" and power >= 0.1:
        box_y -= 5

# Start the Emotiv data processing thread
emotiv_thread = Thread(target=read_emotiv_data, daemon=True)
emotiv_thread.start()

# Game loop
running = True
clock = pygame.time.Clock()  # Initialize Pygame clock for frame rate control
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the box based on its current position
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(400, box_y, 50, 50))

        # Update Pygame display
        pygame.display.flip()

    except Exception as e:
        print(f"Error during game loop: {e}")  # Print any errors encountered

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Close WebSocket connection
ws.close()

# Quit Pygame
pygame.quit()
