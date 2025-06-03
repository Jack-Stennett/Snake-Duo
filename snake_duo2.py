import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Snake initial positions (in grid coordinates)
snake1 = [(5, 5), (4, 5), (3, 5)]  # Snake 1, 3 cells long
snake2 = [(20, 10), (21, 10), (22, 10)]  # Snake 2, 3 cells long

# Directions: (dx, dy)
direction1 = (1, 0)  # Green snake starts moving right
direction2 = (-1, 0) # Red snake starts moving left

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Duo')
clock = pygame.time.Clock()

game_over = False
loser_color = None

def get_random_empty_cell():
    occupied = set(snake1 + snake2)
    num_cells_x = WIDTH // CELL_SIZE
    num_cells_y = HEIGHT // CELL_SIZE
    while True:
        cell = (random.randint(0, num_cells_x - 1), random.randint(0, num_cells_y - 1))
        if cell not in occupied:
            return cell

food = get_random_empty_cell()

def reset_game():
    global snake1, snake2, direction1, direction2, food, game_over, loser_color
    snake1 = [(5, 5), (4, 5), (3, 5)]
    snake2 = [(20, 10), (21, 10), (22, 10)]
    direction1 = (1, 0)
    direction2 = (-1, 0)
    food = get_random_empty_cell()
    game_over = False
    loser_color = None

def main():
    global direction1, direction2, food, game_over, loser_color
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    reset_game()
                    continue  # Skip the rest of the event loop for this frame
                # Red snake (WASD)
                if not game_over:
                    if event.key == pygame.K_w:
                        direction2 = (0, -1)
                    elif event.key == pygame.K_s:
                        direction2 = (0, 1)
                    elif event.key == pygame.K_a:
                        direction2 = (-1, 0)
                    elif event.key == pygame.K_d:
                        direction2 = (1, 0)
                    # Green snake (IJKL)
                    elif event.key == pygame.K_i:
                        direction1 = (0, -1)
                    elif event.key == pygame.K_k:
                        direction1 = (0, 1)
                    elif event.key == pygame.K_j:
                        direction1 = (-1, 0)
                    elif event.key == pygame.K_l:
                        direction1 = (1, 0)

        if game_over:
            screen.fill(BLACK)
            for _ in range(200):  # Number of dots
                x = random.randint(0, WIDTH - CELL_SIZE)
                y = random.randint(0, HEIGHT - CELL_SIZE)
                color = (0, 0, 255) if random.random() < 0.7 else loser_color
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            font = pygame.font.SysFont(None, 48)
            text = font.render("Press R to Restart", True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Skip the rest of the main loop

        # Move green snake
        head1_x, head1_y = snake1[0]
        num_cells_x = WIDTH // CELL_SIZE
        num_cells_y = HEIGHT // CELL_SIZE
        new_head1 = ((head1_x + direction1[0]) % num_cells_x, (head1_y + direction1[1]) % num_cells_y)
        snake1.insert(0, new_head1)
        if new_head1 == food:
            food = get_random_empty_cell()
            # Don't pop tail, snake grows
        else:
            snake1.pop()

        # Move red snake
        head2_x, head2_y = snake2[0]
        new_head2 = ((head2_x + direction2[0]) % num_cells_x, (head2_y + direction2[1]) % num_cells_y)
        snake2.insert(0, new_head2)
        if new_head2 == food:
            food = get_random_empty_cell()
            # Don't pop tail, snake grows
        else:
            snake2.pop()

        # Check for collisions
        if snake1[0] in snake2[1:]:
            game_over = True
            loser_color = GREEN
        elif snake2[0] in snake1[1:]:
            game_over = True
            loser_color = RED

        screen.fill(BLACK)
        # Draw snake 1
        for segment in snake1:
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

        # Draw snake 2
        for segment in snake2:
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, RED, rect)

        # Draw food
        rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 