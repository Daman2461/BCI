import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game Clone")

# Load assets
dinosaur_image = pygame.image.load('doraemon.png')
obstacle_image = pygame.image.load('obstacle.png')
jump_sound = pygame.mixer.Sound('jump_sound.wav')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = dinosaur_image  # Placeholder for the actual dinosaur image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.jump_speed = -18
        self.gravity = 1
        self.velocity = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity = self.jump_speed
            self.jumping = True
            jump_sound.play()

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.y >= SCREEN_HEIGHT - 100:
            self.rect.y = SCREEN_HEIGHT - 100
            self.jumping = False

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=obstacle_image  # Placeholder for the actual obstacle image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -20:
            self.kill()

# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    obstacles = pygame.sprite.Group()
    spawn_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Update game state
        all_sprites.update()
        obstacles.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(player, obstacles):
            running = False

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 100:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            spawn_timer = 0

        # Draw everything
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
