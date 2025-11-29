import pygame
import random
import pygame.freetype

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

#Create emoji font
apple_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)  # For apple🍎
star_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)  # For star⭐
fire_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)  # For fire 🔥
hole_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)  # For black holes ⚫

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
def draw_snake(snake, snake_color, direction):
    for segment in snake[1:]:
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    head = snake[0]
    x = head[0] * CELL_SIZE
    y = head[1] * CELL_SIZE
    radius = CELL_SIZE // 2

    pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

    # Rounded front
    if direction == [1, 0]:  # right
        pygame.draw.circle(screen, snake_color, (x + CELL_SIZE, y + CELL_SIZE // 2), radius)
        eye_y_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_x = x + 3 * CELL_SIZE // 4  # closer to front
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])

    elif direction == [-1, 0]:  # left
        pygame.draw.circle(screen, snake_color, (x, y + CELL_SIZE // 2), radius)
        eye_y_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_x = x + CELL_SIZE // 4  # closer to front (left side)
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])

    elif direction == [0, 1]:  # down
        pygame.draw.circle(screen, snake_color, (x + CELL_SIZE // 2, y + CELL_SIZE), radius)
        eye_x_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_y = y + 3 * CELL_SIZE // 4  # closer to front
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)

    elif direction == [0, -1]:  # up
        pygame.draw.circle(screen, snake_color, (x + CELL_SIZE // 2, y), radius)
        eye_x_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_y = y + CELL_SIZE // 4  # closer to front
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)

    #eyes
    eye_radius = CELL_SIZE // 8
    pygame.draw.circle(screen, BLACK, left_eye, eye_radius)
    pygame.draw.circle(screen, BLACK, right_eye, eye_radius)

# Draw apple
def draw_apple(apple_position):
    # Render emoji
    emoji_surface, emoji_rect = apple_font.render("🍎", RED)
    # Center emoji inside the cell
    emoji_rect.topleft = (apple_position[0] * CELL_SIZE, apple_position[1] * CELL_SIZE)
    screen.blit(emoji_surface, emoji_rect)
    
# Draw special objects
def draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2):
    # Fire emoji
    fire_surface, fire_rect = fire_font.render("🔥", ORANGE)

    cell_x = obstacle_position[0] * CELL_SIZE
    cell_y = obstacle_position[1] * CELL_SIZE
    fire_rect.center = (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2)
    screen.blit(fire_surface, fire_rect)

    # Star emoji
    star_surface, star_rect = star_font.render("⭐", YELLOW)
    star_surface = pygame.transform.scale(star_surface, (CELL_SIZE, CELL_SIZE))
    star_rect.topleft = (star_position[0] * CELL_SIZE, star_position[1] * CELL_SIZE)
    screen.blit(star_surface, star_rect)

    # Black holes emoji
    if black_hole_1 and black_hole_2:
        hole_surface1, hole_rect1 = hole_font.render("⚫", BLACK)
        hole_surface1 = pygame.transform.scale(hole_surface1, (CELL_SIZE, CELL_SIZE))
        hole_rect1.topleft = (black_hole_1[0] * CELL_SIZE, black_hole_1[1] * CELL_SIZE)
        screen.blit(hole_surface1, hole_rect1)

        hole_surface2, hole_rect2 = hole_font.render("⚫", BLACK)
        hole_surface2 = pygame.transform.scale(hole_surface2, (CELL_SIZE, CELL_SIZE))
        hole_rect2.topleft = (black_hole_2[0] * CELL_SIZE, black_hole_2[1] * CELL_SIZE)
        screen.blit(hole_surface2, hole_rect2)

# Main game loop
def game():
    snake = [[10, 10], [9, 10], [8, 10]]
    apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    obstacle_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    direction = [1, 0]
    score = 0

    speed_up = False
    speed_timer = 0
    snake_color = GREEN

    game_running = True
    black_hole_1, black_hole_2 = None, None

    while game_running:
        screen.fill(WHITE)
        draw_grid()
        draw_snake(snake, snake_color, direction)
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

        ate_apple = False

        # 🍎 Apple
        if new_head == apple_position:
            apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            score += 1
            ate_apple = True
            print(f"YAYY!!! You ate an apple 🥳. Score: {score}")

        # ⭐ STAR BONUS — CHANGE COLOR + SPEED
        elif new_head == star_position:
            speed_up = True
            speed_timer = 15 # frames
            snake_color = RED
            star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            print("You have got a speed bonus ⚡⚡")

        # 🔥 Obstacle
        elif new_head == obstacle_position:
            print("You hit an obstacle 💥💀")
            break

        # Spawn black holes
        if score >= 2 and black_hole_1 is None:
            black_hole_1, black_hole_2 = place_black_holes()

        # Teleport
        if black_hole_1 and black_hole_2:
            if new_head == black_hole_1:
                snake[0] = black_hole_2
                black_hole_1, black_hole_2 = place_black_holes()
            elif new_head == black_hole_2:
                snake[0] = black_hole_1
                black_hole_1, black_hole_2 = place_black_holes()

        if not ate_apple:
            snake.pop()

        # ⭐ Handle speed bonus duration
        if speed_up:
            clock.tick(10)
            speed_timer -= 1
            if speed_timer <= 0:
                speed_up = False
                snake_color = GREEN
        else:
            clock.tick(6)

    pygame.quit()

# Run the game
game()
