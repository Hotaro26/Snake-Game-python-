import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(WINDOW_SIZE//2, WINDOW_SIZE//2)]
        self.direction = [GRID_SIZE, 0]
        self.length = 1

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % WINDOW_SIZE, (current[1] + y) % WINDOW_SIZE)
        
        if new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def change_direction(self, direction):
        if direction[0] * -1 != self.direction[0] or direction[1] * -1 != self.direction[1]:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_COUNT-1) * GRID_SIZE,
            random.randint(0, GRID_COUNT-1) * GRID_SIZE
        )

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))

        # Update snake position
        if not snake.update():
            break

        # Check if snake ate food
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        # Draw everything
        screen.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(screen, RED, 
            (food.position[0], food.position[1], GRID_SIZE, GRID_SIZE))
        
        # Draw snake
        for position in snake.positions:
            pygame.draw.rect(screen, GREEN,
                (position[0], position[1], GRID_SIZE, GRID_SIZE))

        # Update display
        pygame.display.flip()
        clock.tick(10)

    # Game Over
    font = pygame.font.Font(None, 50)
    text = font.render(f'Game Over! Score: {score}', True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Wait for a moment before quitting
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()