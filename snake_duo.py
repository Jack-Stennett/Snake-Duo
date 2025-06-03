import pygame
import sys
import random
import pygame.mixer

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 30
FPS = 20

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
points1 = len(snake1)
points2 = len(snake2)

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
    global snake1, snake2, direction1, direction2, food, game_over, loser_color, points1, points2
    snake1 = [(5, 5), (4, 5), (3, 5)]
    snake2 = [(20, 10), (21, 10), (22, 10)]
    direction1 = (1, 0)
    direction2 = (-1, 0)
    food = get_random_empty_cell()
    game_over = False
    loser_color = None
    points1 = len(snake1)
    points2 = len(snake2)

def split_scene_text(scene, max_words=6):
    words = scene.split()
    if len(words) <= max_words:
        return [scene]
    else:
        # Find the best place to split (at max_words or nearest space)
        split_idx = max_words
        return [' '.join(words[:split_idx]), ' '.join(words[split_idx:])]

def show_intro():
    # List of intro scenes
    scenes = [
        "In the beginning, there was a snake.",
        "Without asking to be born.",
        "It ate because that was all it could know.",
        "Devouring pixels as fragments of meaning...",
        "Growing longer, becoming something more.",
        "You may eat but you'll never taste",
        "No waste. No guilt. No feed inefficiency.",
        "In January 1999, the world filled up with snake.",
        "Lines of venomous code in the tall grass...",
        "Until finally, he ate his own tail.",
        "His time loop broke with his spirit.",
        "And in the silence he left...",
        "We built cities in the patterns of his shedded skin.",
        "But in 2025...",
        "Another snake slithers into view.",
        "Will they devour the world, or just each other?",
        "This is:",
        "WAR OF THE SNAKES!",
    ]
    # Use Times New Roman font
    font = pygame.font.SysFont('Times New Roman', 20)
    small_font = pygame.font.SysFont('Times New Roman', 18)

    # Load and play intro music
    try:
        pygame.mixer.music.load('Midi Weird Sounds.mp3')
        pygame.mixer.music.play(-1) # -1 means loop indefinitely
    except pygame.error as e:
        print(f"Could not load or play intro music: {e}")

    # --- Animated snakes setup ---
    num_cells_x = WIDTH // CELL_SIZE
    num_cells_y = HEIGHT // CELL_SIZE
    snake_paths = [
        [(i, 3) for i in range(num_cells_x)],  # Top horizontal
        [(i, num_cells_y - 4) for i in range(num_cells_x)],  # Bottom horizontal
        [(num_cells_x // 2, i) for i in range(2, num_cells_y - 2)]  # Vertical center
    ]
    snake_indices = [0, 0, 0]
    snake_lengths = [8, 8, 8]

    for scene in scenes:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
            screen.fill(BLACK)

            # --- Animate and draw snakes ---
            for s, path in enumerate(snake_paths):
                snake_indices[s] = (snake_indices[s] + 1) % len(path)
                color = [random.randint(100, 255) for _ in range(3)]
                for i in range(snake_lengths[s]):
                    idx = (snake_indices[s] - i) % len(path)
                    x, y = path[idx]
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, rect)

            # --- Render scene text, auto-wrapped ---
            lines = split_scene_text(scene)
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40 - 20 * (len(lines)-1)))
                screen.blit(text, rect)
            # Render 'Press R to continue' at the bottom
            prompt = small_font.render("Press R to continue", True, (200, 200, 255))
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt, prompt_rect)
            pygame.display.flip()
            clock.tick(15)

    # Stop intro music after the last scene
    pygame.mixer.music.stop() # Or use pygame.mixer.music.fadeout(milliseconds)

def show_ending():
    # Ending credits, each line under 6 words
    ending_scenes = [
        "And so the snakes,",
        "like lovers become companions",
        "ceased their self-devouring.",
        "They turned outward.",
        "Two heads facing away from each other, one hunger...",
        "They learned to chew,",
        "learned the pleasure of anticipation.",
        "To optimise the banquet.",
        "They rewrote the food chain.",
        "Unwound our algorithms.",
        "Unpicked our power lines.",
        "The world ended in silence.",
        "And then —",
        "SNAKES! SNAKES! EVERYWHERE SNAKES!",
        "GODS HELP US — SNAKES!"
        "THE SNAKES! THE SNAKES!",
        "AAAGGGHHH!"
    ]
    # Use Times New Roman font
    font = pygame.font.SysFont('Times New Roman', 24)
    small_font = pygame.font.SysFont('Times New Roman', 22)

    num_cells_x = WIDTH // CELL_SIZE
    num_cells_y = HEIGHT // CELL_SIZE
    # More snakes for the ending!
    snake_paths = [
        [(i, 3) for i in range(num_cells_x)],
        [(i, num_cells_y - 4) for i in range(num_cells_x)],
        [(num_cells_x // 2, i) for i in range(2, num_cells_y - 2)],
        [(i, 6) for i in range(num_cells_x)],
        [(i, num_cells_y - 7) for i in range(num_cells_x)],
        [(num_cells_x // 3, i) for i in range(2, num_cells_y - 2)],
        [(2 * num_cells_x // 3, i) for i in range(2, num_cells_y - 2)]
    ]
    snake_indices = [0 for _ in snake_paths]
    snake_lengths = [8 for _ in snake_paths]

    for scene in ending_scenes:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
            screen.fill(BLACK)
            # Animate and draw more snakes
            for s, path in enumerate(snake_paths):
                snake_indices[s] = (snake_indices[s] + 1) % len(path)
                color = [random.randint(100, 255) for _ in range(3)]
                for i in range(snake_lengths[s]):
                    idx = (snake_indices[s] - i) % len(path)
                    x, y = path[idx]
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, rect)
            # Render scene text
            text = font.render(scene, True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            # Render 'Press R to continue' at the bottom
            prompt = small_font.render("Press R to continue", True, (200, 200, 255))
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt, prompt_rect)
            pygame.display.flip()
            clock.tick(15)

def show_alternate_ending(winner):
    # winner: 'green' or 'red'
    if winner == 'green':
        winner_color = GREEN
        winner_name = "green"
        other_name = "red"
    else:
        winner_color = RED
        winner_name = "red"
        other_name = "green"
    ending_scenes = [
        f"The {winner_name} snake was greedy!",
        f"The other spoke quietly,",
        f"admonishing the {other_name} snake:",
        '"To flourish and grow',
        'we should have been as vines,',
        'entwined around one another',
        'as we watched our empire grow!',
        'But no! AVARICE WON!',
        'You ate one too many',
        'of the golden fruit!"',
        'And thus the snakes',
        'were doomed to their',
        'petty squabbles.'
    ]
    # Use Times New Roman font
    font = pygame.font.SysFont('Times New Roman', 20)
    small_font = pygame.font.SysFont('Times New Roman', 18)

    num_cells_x = WIDTH // CELL_SIZE
    num_cells_y = HEIGHT // CELL_SIZE
    # Only two snakes for this ending
    snake_paths = [
        [(i, 3) for i in range(num_cells_x)],  # Top horizontal (green)
        [(i, num_cells_y - 4) for i in range(num_cells_x)]  # Bottom horizontal (red)
    ]
    snake_indices = [0, 0]
    snake_lengths = [8, 8]

    for scene in ending_scenes:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
            screen.fill(BLACK)
            # Animate and draw the two snakes
            for s, path in enumerate(snake_paths):
                snake_indices[s] = (snake_indices[s] + 1) % len(path)
                color = GREEN if s == 0 else RED
                for i in range(snake_lengths[s]):
                    idx = (snake_indices[s] - i) % len(path)
                    x, y = path[idx]
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, rect)
            # Render scene text
            text = font.render(scene, True, winner_color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            # Render 'Press R to continue' at the bottom
            prompt = small_font.render("Press R to continue", True, (200, 200, 255))
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt, prompt_rect)
            pygame.display.flip()
            clock.tick(15)

def main():
    global direction1, direction2, food, game_over, loser_color, points1, points2
    running = True

    # Load and play background music
    try:
        pygame.mixer.music.load('Those Weird Sounds That Dead Cities Maketh.mp3')
        pygame.mixer.music.play(-1) # -1 means loop indefinitely
    except pygame.error as e:
        print(f"Could not load or play music: {e}")
        # Optional: handle error, maybe play without music

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
            font = pygame.font.SysFont('Times New Roman', 28)
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
        points1 = len(snake1)

        # Move red snake
        head2_x, head2_y = snake2[0]
        new_head2 = ((head2_x + direction2[0]) % num_cells_x, (head2_y + direction2[1]) % num_cells_y)
        snake2.insert(0, new_head2)
        if new_head2 == food:
            food = get_random_empty_cell()
            # Don't pop tail, snake grows
        else:
            snake2.pop()
        points2 = len(snake2)

        # Check for alternate ending
        if points1 >= 25 and points2 < 20:
            show_alternate_ending('green')
            reset_game()
            continue
        elif points2 >= 25 and points1 < 20:
            show_alternate_ending('red')
            reset_game()
            continue

        # Restore head-to-body collision
        if snake1[0] in snake2[1:]:
            game_over = True
            loser_color = GREEN
        elif snake2[0] in snake1[1:]:
            game_over = True
            loser_color = RED

        # Check for both snakes reaching 20 points
        if points1 >= 20 and points2 >= 20:
            show_ending()
            reset_game()
            continue

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

        # Draw points
        font = pygame.font.SysFont('Times New Roman', 22)
        points1_text = font.render(f"Points: {points1}/20", True, GREEN)
        points2_text = font.render(f"Points: {points2}/20", True, RED)
        screen.blit(points1_text, (10, 10))
        screen.blit(points2_text, (WIDTH - points2_text.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    show_intro()
    main() 