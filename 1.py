import pygame
import sys
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup - fixed size window
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Create sound objects for ball collisions
paddle_hit_sound = generate_beep_sound(440, 0.1)  # A4
wall_hit_sound = generate_beep_sound(523.25, 0.1)  # C5
score_sound = generate_beep_sound(880, 0.2)  # A5

# Set up some constants
BALL_SIZE = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the paddles
paddle1 = pygame.Rect(30, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect((SCREEN_WIDTH - BALL_SIZE) // 2, (SCREEN_HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [2, 2]

# Set up the font for displaying text
font = pygame.font.Font(None, 36)

# Set up the scores
score1 = 0
score2 = 0

# Set up the game state
game_state = "start"  # "start", "play", "game_over"

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == "start" and event.key == pygame.K_SPACE:
                game_state = "play"
            elif game_state == "game_over" and event.key == pygame.K_SPACE:
                game_state = "start"
                score1 = 0
                score2 = 0
                ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_speed = [2, 2]

    if game_state == "start":
        # Display the start screen
        start_text = font.render("Press SPACE to start", True, WHITE)
        text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(start_text, text_rect)
    elif game_state == "play":
        # Move the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle1.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            paddle1.move_ip(0, 5)
        if keys[pygame.K_w]:
            paddle2.move_ip(0, -5)
        if keys[pygame.K_s]:
            paddle2.move_ip(0, 5)

        # Keep the paddles on the screen
        if paddle1.top <= 0:
            paddle1.top = 0
        if paddle1.bottom >= SCREEN_HEIGHT:
            paddle1.bottom = SCREEN_HEIGHT
        if paddle2.top <= 0:
            paddle2.top = 0
        if paddle2.bottom >= SCREEN_HEIGHT:
            paddle2.bottom = SCREEN_HEIGHT

        # Move the ball
        ball.move_ip(ball_speed)

        # Bounce the ball off the top and bottom of the screen
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed[1] = -ball_speed[1]
            wall_hit_sound.play()

        # Bounce the ball off the paddles
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed[0] = -ball_speed[0]
            paddle_hit_sound.play()

        # Check for scoring
        if ball.left <= 0:
            score2 += 1
            score_sound.play()
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed = [-2, 2]
        elif ball.right >= SCREEN_WIDTH:
            score1 += 1
            score_sound.play()
            ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball_speed = [2, 2]

        # Check for game over
        if score1 >= 11 or score2 >= 11:
            game_state = "game_over"

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the paddles and ball
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw the center line
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Draw the scores
        score_text1 = font.render(str(score1), True, WHITE)
        score_text2 = font.render(str(score2), True, WHITE)
        screen.blit(score_text1, (SCREEN_WIDTH // 4, 10))
        screen.blit(score_text2, (SCREEN_WIDTH * 3 // 4, 10))
    elif game_state == "game_over":
        # Display the game over screen
        game_over_text = font.render("Game Over - Press SPACE to restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)

    # Flip the display
    pygame.display.flip()
    
    # Cap the frame rate at 60 FPS
    clock.tick(60)
