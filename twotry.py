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

# Function to place black holes with a minimum distance
def place_black_holes():
    while True:
        black_hole_1 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        black_hole_2 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        distance = abs(black_hole_1[0] - black_hole_2[0]) + abs(black_hole_1[1] - black_hole_2[1])
        if distance >= 5:  # Ensure a minimum distance of 5 units
            return black_hole_1, black_hole_2

# Function to draw the snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the apple
def draw_apple(apple_position):
    pygame.draw.rect(screen, RED, pygame.Rect(apple_position[0] * CELL_SIZE, apple_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw obstacles, stars, and black holes
def draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2):
    pygame.draw.rect(screen, ORANGE, pygame.Rect(obstacle_position[0] * CELL_SIZE, obstacle_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Fire
    pygame.draw.rect(screen, YELLOW, pygame.Rect(star_position[0] * CELL_SIZE, star_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Star
    if black_hole_1 and black_hole_2:  # Only draw black holes if they have been initialized
        pygame.draw.rect(screen, WHITE, pygame.Rect(black_hole_1[0] * CELL_SIZE, black_hole_1[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, WHITE, pygame.Rect(black_hole_2[0] * CELL_SIZE, black_hole_2[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
def game():
    # Initialize the game variables
    snake = [[10, 10], [9, 10], [8, 10]]
    apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    obstacle_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    direction = [1, 0]  # Initial direction: moving right
    score = 0
    game_running = True
    black_hole_1, black_hole_2 = None, None
    last_apple_eaten = 0  # To track apples eaten
    speed_up = False  # To track whether the snake is in speed up mode

    while game_running:
        screen.fill(BLACK)  # Fill the screen with black
        draw_grid()  # Draw the grid
        draw_snake(snake)  # Draw the snake
        draw_apple(apple_position)  # Draw the apple
        draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2)  # Draw obstacles, stars, and black holes
        
        pygame.display.update()  # Update the display
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Up
                    direction = [0, -1]
                elif event.key == pygame.K_s:  # Down
                    direction = [0, 1]
                elif event.key == pygame.K_a:  # Left
                    direction = [-1, 0]
                elif event.key == pygame.K_d:  # Right
                    direction = [1, 0]

        # Calculate the new position of the snake
        head = snake[0]
        new_head = [head[0] + direction[0], head[1] + direction[1]]

        # Check for collision with the border or self
        if new_head in snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= GRID_SIZE or new_head[1] >= GRID_SIZE:
            game_running = False
            print("💥 GAME OVER! 💀")

        # Add the new head to the snake
        snake.insert(0, new_head)

        # Check if the snake eats the apple
        if new_head == apple_position:
            last_apple_eaten += 1
            apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
            score += 1
            print(f"YAYY!!! You ate an apple 🥳. Score: {score}")
        
        # Check if the snake eats the star (speed boost)
        elif new_head == star_position:
            speed_up = True  # Set to true when the snake eats the star
            print('You have got a speed bonus ⚡⚡')
            star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        
        # Check if the snake hits an obstacle
        elif new_head == obstacle_position:
            game_running = False
            print("You hit an obstacle 💥💀")

        # Add black holes after eating 2 apples
        if last_apple_eaten >= 2 and black_hole_1 is None and black_hole_2 is None:
            black_hole_1, black_hole_2 = place_black_holes()

        # Check if the snake enters a black hole
        if black_hole_1 and black_hole_2:  # Only check for black holes after they are placed
            if new_head == black_hole_1:
                print('You entered a white hole! Teleporting to the other side... ⚪➡️⚪')
                snake[0] = black_hole_2  # Teleport to the other white hole
                black_hole_1, black_hole_2 = place_black_holes()  # Randomly reposition black holes
                print(f'White holes have swapped! New positions: {black_hole_1}, {black_hole_2}')
            elif new_head == black_hole_2:
                print('You entered a white hole! Teleporting to the other side... ⚪➡️⚪')
                snake[0] = black_hole_1  # Teleport to the other white hole
                black_hole_1, black_hole_2 = place_black_holes()  # Randomly reposition black holes
                print(f'White holes have swapped! New positions: {black_hole_1}, {black_hole_2}')
        
        # Remove the snake's tail (if no apple was eaten)
        if new_head != apple_position:
            snake.pop()

        # Control the game speed (lower FPS for slower game)
        if speed_up:
            clock.tick(10)  # Faster speed after eating the star
        else:
            clock.tick(3)  # Slow down to 3 FPS (frames per second)

    pygame.quit()

# Run the game
game()
