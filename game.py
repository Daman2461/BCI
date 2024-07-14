import pygame
import random
import math
import threading
import queue
import backend
import sys
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FONT = pygame.font.SysFont('consolas', 50)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BCI Game")

# Load assets
background_image = pygame.image.load('bg.png').convert()
bg_width = background_image.get_width()

tiles = math.ceil(SCREEN_WIDTH / bg_width)
def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(frame, (128, 128))
        frames.append(scaled_frame)
         
    return frames


sprite_sheet = pygame.image.load('run.png')
running_frames = load_sprite_sheet(sprite_sheet, 32, 32, 12)

obstacle_image = pygame.image.load('obstacle.png')
jump_sound = pygame.mixer.Sound('jump_sound.wav')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.frames = running_frames
        self.image = self.frames[0] 
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 120
        self.jump_speed = -25            
        self.gravity = 1
        self.velocity = 0
        self.jumping = False
        self.frame_index = 0
        self.animation_speed = 0.7
        self.time = 0

    def jump(self):
        if not self.jumping:
            self.velocity = self.jump_speed
            self.jumping = True
            jump_sound.play()

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.y >= SCREEN_HEIGHT - 120:
            self.rect.y = SCREEN_HEIGHT - 120
            self.jumping = False

        self.time += self.animation_speed
        if self.time >= 1:
            self.time = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image  # Placeholder for the actual obstacle image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -20:
            self.kill()

# Command queue
command_queue = queue.Queue()

def handle_commands(player):
    while True:
        command = command_queue.get()
        if command == 'move_up':
            player.jump()

# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    obstacles = pygame.sprite.Group()
    spawn_timer = 0
    scroll = 0
    p=False
    run=True
    c=0
    # Start WebSocket in a separate thread
    ws_thread = threading.Thread(target=backend.process_data, args=(command_queue,))
    ws_thread.start()

    # Start command handler in a separate thread
    command_thread = threading.Thread(target=handle_commands, args=(player,))
    command_thread.start()

    while running:
        

        # Update game state
        if run==True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                        
                        if event.key==pygame.K_p:
                            p=True
                            run=False
            all_sprites.update()
            obstacles.update()

            # Check for collisions
            if pygame.sprite.spritecollideany(player, obstacles):
                run = False
                continue

            # Spawn obstacles
            spawn_timer += 1
            if spawn_timer > 100:
                c+=1
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                spawn_timer = 0

            # Scrolling background image
            for i in range(tiles):
                screen.blit(background_image, (i * bg_width + scroll, 0))
            scroll -= 4
            if abs(scroll) > bg_width:
                scroll = 0

            # Draw everything
            all_sprites.draw(screen)
            score=FONT.render(str(c),1,WHITE)
            screen.blit(score,(SCREEN_WIDTH//2-20 , 50))
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(25)
        else:
            if p==False:
                screen.blit(FONT.render("""PRESS SPACE TO RESTART """,1,WHITE),(125,SCREEN_HEIGHT//2))
                 
                pygame.display.flip()
            else:
                screen.blit(FONT.render("""PRESS SPACE TO RESUME """,1,WHITE),(125,SCREEN_HEIGHT//2))
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = True
                        clock = pygame.time.Clock()
                        player = Player()
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(player)
                        obstacles = pygame.sprite.Group()
                        spawn_timer = 0
                        scroll = 0
                        
                        run=True
                        
                        if p==False: 
                            c=0
                            continue
                        else:
                            
                            p=False
                            continue


    pygame.quit()
    
    sys.exit()
    quit()

if __name__ == '__main__':
    main()
