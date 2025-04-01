import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Spaceship Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ship_size = 30
ship_x = WIDTH // 2
ship_y = HEIGHT // 2
ship_speed = 5

def main():
    global ship_x, ship_y
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            ship_y -= ship_speed
        if keys[pygame.K_s]:
            ship_y += ship_speed
        if keys[pygame.K_a]:
            ship_x -= ship_speed
        if keys[pygame.K_d]:
            ship_x += ship_speed
        
        ship_x = max(ship_size // 2, min(ship_x, WIDTH - ship_size // 2))
        ship_y = max(ship_size // 2, min(ship_y, HEIGHT - ship_size // 2))
        
        screen.fill(BLACK)
        
        points = [
            (ship_x, ship_y - ship_size // 2),
            (ship_x - ship_size // 2, ship_y + ship_size // 2),
            (ship_x + ship_size // 2, ship_y + ship_size // 2)
        ]
        pygame.draw.polygon(screen, WHITE, points)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()