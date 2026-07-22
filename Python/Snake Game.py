"""
Snake Game
----------
Classic Snake game built with Pygame.

Controls:
    Arrow Keys / WASD - Move the snake
    P                 - Pause / Unpause
    R                 - Restart after Game Over
    Esc / Close Window - Quit

Requirements:
    pip install pygame
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10  # Base speed; increases slightly as the snake grows

# Colors (R, G, B)
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GREEN_HEAD = (100, 220, 100)
GREEN_BODY = (60, 170, 70)
RED = (220, 70, 70)
GRAY = (40, 40, 48)
YELLOW = (240, 200, 60)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x, start_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def set_direction(self, new_dir):
        # Prevent the snake from reversing directly into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.pending_direction = new_dir

    def move(self):
        self.direction = self.pending_direction
        head_x, head_y = self.head()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def check_self_collision(self):
        return self.head() in self.body[1:]

    def check_wall_collision(self):
        x, y = self.head()
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT


class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.respawn(snake_body)

    def respawn(self, snake_body):
        available = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_body
        ]
        self.position = random.choice(available) if available else None


def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_cell(surface, pos, color):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect, border_radius=4)


def draw_snake(surface, snake):
    for i, segment in enumerate(snake.body):
        color = GREEN_HEAD if i == 0 else GREEN_BODY
        draw_cell(surface, segment, color)


def draw_text_center(surface, text, font, color, y_offset=0):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(rendered, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    font_large = pygame.font.SysFont("arial", 48, bold=True)
    font_medium = pygame.font.SysFont("arial", 28)
    font_small = pygame.font.SysFont("arial", 20)

    snake = Snake()
    food = Food(snake.body)
    score = 0
    high_score = 0
    game_over = False
    paused = False

    key_directions = {
        pygame.K_UP: UP,
        pygame.K_w: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_d: RIGHT,
    }

    running = True
    while running:
        # --- Event handling -------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in key_directions and not game_over and not paused:
                    snake.set_direction(key_directions[event.key])
                elif event.key == pygame.K_p and not game_over:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    snake.reset()
                    food.respawn(snake.body)
                    score = 0
                    game_over = False
                    paused = False

        # --- Update -----------------------------------------------------------
        if not game_over and not paused:
            snake.move()

            if snake.check_wall_collision() or snake.check_self_collision():
                game_over = True
                high_score = max(high_score, score)
            elif food.position and snake.head() == food.position:
                snake.grow(1)
                score += 10
                food.respawn(snake.body)

        # --- Draw ---------------------------------------------------------
        screen.fill(BLACK)
        draw_grid(screen)

        if food.position:
            draw_cell(screen, food.position, RED)

        draw_snake(screen, snake)

        score_surf = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if paused and not game_over:
            draw_text_center(screen, "PAUSED", font_large, YELLOW)
        elif game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            draw_text_center(screen, "GAME OVER", font_large, RED, y_offset=-40)
            draw_text_center(screen, f"Score: {score}   High Score: {high_score}", font_medium, WHITE, y_offset=10)
            draw_text_center(screen, "Press R to Restart or Esc to Quit", font_small, WHITE, y_offset=50)

        pygame.display.flip()

        # Speed scales gently with snake length for a bit of extra challenge
        current_fps = FPS + len(snake.body) // 5
        clock.tick(current_fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()