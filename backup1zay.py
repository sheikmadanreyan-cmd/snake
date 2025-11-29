import pygame
import random
import pygame.freetype
import time
import os

# ---- init ----
pygame.init()

# ---- colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN  = (0, 255, 255)   # you chose cyan
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# ---- constants ----
GRID_SIZE = 20
CELL_SIZE = 30
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

# ---- window ----
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# ---- emoji fonts ----
apple_font = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
star_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
fire_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)
hole_font  = pygame.freetype.SysFont("segoeuisymbol", CELL_SIZE)

# ---- score font ----
score_font = pygame.freetype.SysFont("Arial", 22)

# ---- clock ----
clock = pygame.time.Clock()

# ---- high score file helpers ----
HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or "0")
    except Exception:
        return 0

def save_high_score(n):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(int(n)))
    except Exception:
        pass

HIGH_SCORE = load_high_score()

# ---- helper: place black holes (min distance 5) ----
def place_black_holes():
    while True:
        b1 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        b2 = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
        distance = abs(b1[0]-b2[0]) + abs(b1[1]-b2[1])
        if distance >= 5:
            return b1, b2

# ---- draw grid ----
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# ---- draw snake (with rounded head + eyes), uses boosted flag to select color ----
def draw_snake(snake, direction, boosted):
    body_color = CYAN if boosted else GREEN

    # draw body segments (skip head)
    for segment in snake[1:]:
        pygame.draw.rect(screen, body_color,
                         pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # draw head (square + rounded front)
    head = snake[0]
    x = head[0] * CELL_SIZE
    y = head[1] * CELL_SIZE
    radius = CELL_SIZE // 2

    pygame.draw.rect(screen, body_color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

    # rounded front & eyes depending on direction
    if direction == [1, 0]:  # right
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE, y + CELL_SIZE // 2), radius)
        eye_y_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_x = x + 3 * CELL_SIZE // 4
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])
    elif direction == [-1, 0]:  # left
        pygame.draw.circle(screen, body_color, (x, y + CELL_SIZE // 2), radius)
        eye_y_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_x = x + CELL_SIZE // 4
        left_eye = (eye_x, y + eye_y_offsets[0])
        right_eye = (eye_x, y + eye_y_offsets[1])
    elif direction == [0, 1]:  # down
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE // 2, y + CELL_SIZE), radius)
        eye_x_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_y = y + 3 * CELL_SIZE // 4
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)
    else:  # up
        pygame.draw.circle(screen, body_color, (x + CELL_SIZE // 2, y), radius)
        eye_x_offsets = [CELL_SIZE // 3, 2 * CELL_SIZE // 3]
        eye_y = y + CELL_SIZE // 4
        left_eye = (x + eye_x_offsets[0], eye_y)
        right_eye = (x + eye_x_offsets[1], eye_y)

    eye_radius = CELL_SIZE // 8
    pygame.draw.circle(screen, BLACK, left_eye, eye_radius)
    pygame.draw.circle(screen, BLACK, right_eye, eye_radius)

# ---- draw apple emoji ----
def draw_apple(apple_position):
    surf, rect = apple_font.render("🍎", RED)
    rect.topleft = (apple_position[0] * CELL_SIZE, apple_position[1] * CELL_SIZE)
    screen.blit(surf, rect)

# ---- draw star, fire, holes ----
def draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2):
    # fire emoji (centered)
    fire_surf, fire_rect = fire_font.render("🔥", ORANGE)
    fire_rect.center = (obstacle_position[0]*CELL_SIZE + CELL_SIZE//2, obstacle_position[1]*CELL_SIZE + CELL_SIZE//2)
    screen.blit(fire_surf, fire_rect)

    # star
    star_surf, star_rect = star_font.render("⭐", YELLOW)
    star_surf = pygame.transform.scale(star_surf, (CELL_SIZE, CELL_SIZE))
    star_rect.topleft = (star_position[0]*CELL_SIZE, star_position[1]*CELL_SIZE)
    screen.blit(star_surf, star_rect)

    # holes
    if black_hole_1 and black_hole_2:
        hole_surf1, hole_rect1 = hole_font.render("⚫", BLACK)
        hole_surf1 = pygame.transform.scale(hole_surf1, (CELL_SIZE, CELL_SIZE))
        hole_rect1.topleft = (black_hole_1[0]*CELL_SIZE, black_hole_1[1]*CELL_SIZE)
        screen.blit(hole_surf1, hole_rect1)

        hole_surf2, hole_rect2 = hole_font.render("⚫", BLACK)
        hole_surf2 = pygame.transform.scale(hole_surf2, (CELL_SIZE, CELL_SIZE))
        hole_rect2.topleft = (black_hole_2[0]*CELL_SIZE, black_hole_2[1]*CELL_SIZE)
        screen.blit(hole_surf2, hole_rect2)

# ---- draw score + high score ----
def draw_score_and_high(score, high_score):
    score_surf, score_rect = score_font.render(f"Score: {score}", BLACK)
    screen.blit(score_surf, (8, 6))
    high_surf, high_rect = score_font.render(f"High Score: {high_score}", BLACK)
    screen.blit(high_surf, (8, 30))

# ---- main game ----
def game():
    global HIGH_SCORE

    snake = [[10, 10], [9, 10], [8, 10]]
    apple_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    obstacle_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    star_position = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
    direction = [1, 0]
    score = 0

    # speeds
    normal_rate = 5   # slightly slower normal speed
    boost_extra = 5   # how much faster during boost

    boosted = False
    boost_end_time = 0

    black_hole_1 = None
    black_hole_2 = None

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_snake(snake, direction, boosted)
        draw_apple(apple_position)
        draw_specials(obstacle_position, star_position, black_hole_1, black_hole_2)
        draw_score_and_high(score, HIGH_SCORE)
        pygame.display.update()

        # events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_w, pygame.K_UP):
                    # prevent immediate reverse
                    if direction != [0, 1]:
                        direction = [0, -1]
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    if direction != [0, -1]:
                        direction = [0, 1]
                elif ev.key in (pygame.K_a, pygame.K_LEFT):
                    if direction != [1, 0]:
                        direction = [-1, 0]
                elif ev.key in (pygame.K_d, pygame.K_RIGHT):
                    if direction != [-1, 0]:
                        direction = [1, 0]

        # move snake
        head = snake[0]
        new_head = [head[0] + direction[0], head[1] + direction[1]]

        # collision with self or wall
        if new_head in snake or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= GRID_SIZE or new_head[1] >= GRID_SIZE:
            print("💥 GAME OVER! 💀")
            break

        snake.insert(0, new_head)

        ate_apple = False

        # apple eat -> grow + respawn (avoid naive repeat)
        if new_head == apple_position:
            ate_apple = True
            score += 1
            # immediate high score update (live)
            if score > HIGH_SCORE:
                HIGH_SCORE = score
                save_high_score(HIGH_SCORE)
            # respawn apple (simple random; could be improved to avoid conflicts)
            while True:
                candidate = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
                if candidate not in snake and candidate != obstacle_position and candidate != star_position:
                    apple_position = candidate
                    break
            print(f"YAYY!!! You ate an apple 🥳. Score: {score}")

        # star eaten -> boost for 3 seconds; place star before enabling boost to avoid immediate retrigger
        elif new_head == star_position:
            # respawn star to a free cell
            while True:
                candidate = [random.randint(1, GRID_SIZE-2), random.randint(1, GRID_SIZE-2)]
                if candidate not in snake and candidate != apple_position and candidate != obstacle_position:
                    star_position = candidate
                    break
            boosted = True
            boost_end_time = time.time() + 3.0
            print("You have got a speed bonus ⚡⚡ (3s)")

        # hit obstacle -> game over
        elif new_head == obstacle_position:
            print("You hit an obstacle 💥💀")
            break

        # spawn black holes after score >= 2
        if score >= 2 and black_hole_1 is None:
            black_hole_1, black_hole_2 = place_black_holes()

        # teleport if enter hole
        if black_hole_1 and black_hole_2:
            if new_head == black_hole_1:
                snake[0] = black_hole_2.copy()
                black_hole_1, black_hole_2 = place_black_holes()
            elif new_head == black_hole_2:
                snake[0] = black_hole_1.copy()
                black_hole_1, black_hole_2 = place_black_holes()

        # remove tail if not eaten apple (grows by 1 when apple eaten)
        if not ate_apple:
            snake.pop()

        # turn off boost after 3 seconds
        if boosted and time.time() > boost_end_time:
            boosted = False

        # control speed (boosted -> a bit faster)
        if boosted:
            clock.tick(normal_rate + boost_extra)
        else:
            clock.tick(normal_rate)

    # end of game: check high score (already updated live, but ensure saved)
    if score > HIGH_SCORE:
        HIGH_SCORE = score
        save_high_score(HIGH_SCORE)
        print(f"🎉 NEW HIGH SCORE: {HIGH_SCORE}")

    pygame.quit()

# ---- start ----
game()
