import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
GRID_SIZE = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Color for the star
ORANGE = (255, 165, 0)  # Color for the fire (obstacle)
GRAY = (169, 169, 169)

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Place black holes
def place_black_holes():
    while True:
        black_hole_1 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        black_hole_2 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        distance = abs(black_hole_1[0] - black_hole_2[0]) + abs(black_hole_1[1] - black_hole_2[1])
        if distance >= 5:
            return black_hole_1, black_hole_2

# Draw snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw apple
def draw_apple(apple_position):
    pygame.draw.rect(screen, RED, pygame.Rect(apple_position[0] * CELL_SIZE, apple_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw star, fire, black holes
def draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2):
    pygame.draw.rect(screen, ORANGE, pygame.Rect(obstacle_position[0] * CELL_SIZE, obstacle_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(star_position[0] * CELL_SIZE, star_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if black_hole_1 and black_hole_2:
        pygame.draw.rect(screen, WHITE, pygame.Rect(black_hole_1[0] * CELL_SIZE, black_hole_1[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, WHITE, pygame.Rect(black_hole_2[0] * CELL_SIZE, black_hole_2[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
def game():
    snake = [[10, 10], [9, 10], [8, 10]]
    apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    obstacle_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    direction = [1, 0]
    score = 0
    speed_up = False
    game_running = True
    black_hole_1, black_hole_2 = None, None

    while game_running:
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_apple(apple_position)
        draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    direction = [0, -1]
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    direction = [0, 1]
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    direction = [-1, 0]
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    direction = [1, 0]

        head = snake[0]
        new_head = [head[0] + direction[0], head[1] + direction[1]]

        # Collision detection
        if new_head in snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= GRID_SIZE or new_head[1] >= GRID_SIZE:
            print("💥 GAME OVER! 💀")
            break

        snake.insert(0, new_head)

        # Track if apple was eaten (needed so we don't pop tail)
        ate_apple = False

        # 🍎 APPLE EAT — GROW SNAKE
        if new_head == apple_position:
            apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            score += 1
            ate_apple = True  # ❗MARK — so tail is NOT removed
            print(f"YAYY!!! You ate an apple 🥳. Score: {score}")

        # ⭐ STAR SPEED BOOST
        elif new_head == star_position:
            speed_up = True
            star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            print("You have got a speed bonus ⚡⚡")

        # 🔥 OBSTACLE
        elif new_head == obstacle_position:
            print("You hit an obstacle 💥💀")
            break

        # Black holes appear after score >= 2
        if score >= 2 and black_hole_1 is None:
            black_hole_1, black_hole_2 = place_black_holes()

        # White hole teleport
        if black_hole_1 and black_hole_2:
            if new_head == black_hole_1:
                snake[0] = black_hole_2
                black_hole_1, black_hole_2 = place_black_holes()
            elif new_head == black_hole_2:
                snake[0] = black_hole_1
                black_hole_1, black_hole_2 = place_black_holes()

        # 🟢 REMOVE TAIL ONLY IF NO APPLE WAS EATEN
        if not ate_apple:
            snake.pop()

        # Speed control
        if speed_up:
            clock.tick(10)
        else:
            clock.tick(3)

    pygame.quit()

# Run the game
game()
