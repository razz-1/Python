"""
Pong Game
=========
A classic two-player Pong game built with pygame.

Controls:
    Player 1 (left paddle):  W (up) / S (down)
    Player 2 (right paddle): UP ARROW / DOWN ARROW
    P: Pause
    R: Restart after game over
    ESC / close window: Quit

First player to reach the winning score (default 5) wins.

Requirements:
    pip install pygame
"""

import pygame
import random
import sys

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
BALL_SPEEDUP_FACTOR = 1.05  # Ball speeds up slightly on each paddle hit
BALL_MAX_SPEED = 15

WINNING_SCORE = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 215, 0)

FONT_NAME = None  # Use pygame's default font


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2,
            SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.reset()

    def reset(self, direction=None):
        """Reset the ball to the center with a random angle."""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        if direction is None:
            direction = random.choice([-1, 1])

        angle = random.uniform(-0.4, 0.4)  # radians, limits steepness
        self.speed_x = BALL_SPEED_X * direction
        self.speed_y = BALL_SPEED_Y * (1 if random.random() > 0.5 else -1)
        self.speed_y *= abs(angle) / 0.4 if angle != 0 else 0.5

    def move(self):
        self.rect.x += int(self.speed_x)
        self.rect.y += int(self.speed_y)

        # Bounce off top/bottom walls
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def speed_up(self):
        speed_multiplier = BALL_SPEEDUP_FACTOR
        new_speed_x = self.speed_x * speed_multiplier
        new_speed_y = self.speed_y * speed_multiplier

        # Cap max speed
        if abs(new_speed_x) < BALL_MAX_SPEED:
            self.speed_x = new_speed_x
        if abs(new_speed_y) < BALL_MAX_SPEED:
            self.speed_y = new_speed_y


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.font_large = pygame.font.Font(FONT_NAME, 72)
        self.font_medium = pygame.font.Font(FONT_NAME, 36)
        self.font_small = pygame.font.Font(FONT_NAME, 24)

        self.reset_game()

    def reset_game(self):
        self.left_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(
            SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.ball = Ball()
        self.left_score = 0
        self.right_score = 0
        self.paused = False
        self.game_over = False
        self.winner = None

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.paused and not self.game_over:
            # Player 1 controls (W/S)
            if keys[pygame.K_w]:
                self.left_paddle.move(-self.left_paddle.speed)
            if keys[pygame.K_s]:
                self.left_paddle.move(self.left_paddle.speed)

            # Player 2 controls (Arrow keys)
            if keys[pygame.K_UP]:
                self.right_paddle.move(-self.right_paddle.speed)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(self.right_paddle.speed)

    def update(self):
        if self.paused or self.game_over:
            return

        self.ball.move()

        # Check collision with left paddle
        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.speed_x < 0:
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.speed_x *= -1
            self._adjust_bounce_angle(self.left_paddle)
            self.ball.speed_up()

        # Check collision with right paddle
        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.speed_x > 0:
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.speed_x *= -1
            self._adjust_bounce_angle(self.right_paddle)
            self.ball.speed_up()

        # Check scoring
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self._check_game_over()
            if not self.game_over:
                self.ball.reset(direction=1)

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.left_score += 1
            self._check_game_over()
            if not self.game_over:
                self.ball.reset(direction=-1)

    def _adjust_bounce_angle(self, paddle):
        """Adjust the ball's Y speed based on where it hit the paddle."""
        relative_intersect = (paddle.rect.centery - self.ball.rect.centery) / (
            PADDLE_HEIGHT / 2
        )
        # Clamp between -1 and 1, then invert so top hit = ball goes up
        relative_intersect = max(-1, min(1, relative_intersect))
        self.ball.speed_y = -relative_intersect * BALL_SPEED_Y * 1.5

    def _check_game_over(self):
        if self.left_score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 1"
        elif self.right_score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 2"

    def draw_center_line(self):
        dash_height = 15
        gap = 10
        x = SCREEN_WIDTH // 2
        y = 0
        while y < SCREEN_HEIGHT:
            pygame.draw.rect(self.screen, GRAY, (x - 2, y, 4, dash_height))
            y += dash_height + gap

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_center_line()

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Draw scores
        left_text = self.font_large.render(str(self.left_score), True, WHITE)
        right_text = self.font_large.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (SCREEN_WIDTH // 4 - left_text.get_width() // 2, 20))
        self.screen.blit(
            right_text, (3 * SCREEN_WIDTH // 4 - right_text.get_width() // 2, 20)
        )

        # Draw instructions
        instructions = self.font_small.render(
            "W/S: Player 1   |   UP/DOWN: Player 2   |   P: Pause", True, GRAY
        )
        self.screen.blit(
            instructions,
            (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 30),
        )

        if self.paused and not self.game_over:
            pause_text = self.font_medium.render("PAUSED", True, YELLOW)
            self.screen.blit(
                pause_text,
                (
                    SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - pause_text.get_height() // 2,
                ),
            )

        if self.game_over:
            win_text = self.font_large.render(f"{self.winner} Wins!", True, YELLOW)
            restart_text = self.font_medium.render("Press R to Restart", True, WHITE)
            self.screen.blit(
                win_text,
                (
                    SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 60,
                ),
            )
            self.screen.blit(
                restart_text,
                (
                    SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 20,
                ),
            )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p:
                        if not self.game_over:
                            self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        if self.game_over:
                            self.reset_game()

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PongGame()
    game.run()