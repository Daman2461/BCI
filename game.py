import pygame
import threading
import queue
import backend

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("BCI Controlled Game")

# Set up assets
player = pygame.Rect(375, 525, 50, 50)
velocity = 5

# Command queue
command_queue = queue.Queue()

# Game loop
running = True

def handle_commands():
    while True:
        command = command_queue.get()
        if command == 'move_up':
            player.y -= velocity
        elif command == 'stay':
            pass  # Do nothing if the command is 'stay'

# Start WebSocket in a separate thread
ws_thread = threading.Thread(target=backend.process_data, args=(command_queue,))
ws_thread.start()

# Start command handler in a separate thread
command_thread = threading.Thread(target=handle_commands)
command_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    window.fill((0, 0, 0))
    
    # Draw player
    pygame.draw.rect(window, (255, 0, 0), player)
    
    # Update display
    pygame.display.update()

    # Sleep briefly to control the game loop speed
    pygame.time.delay(50)

# Quit Pygame
pygame.quit()
