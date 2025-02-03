import pygame, math
from pygame.locals import *

pygame.init()

# USED MUSICS
pygame.mixer.music.load("BGmusic.mp3") # Not available on Mac
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(1)

hit_sound = pygame.mixer.Sound('Pong.wav')
hit_sound.set_volume(0.5)

# USED COLORS
ORANGE = (255, 140, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Set screen and caption
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong-Game")
game_active = True

clock = pygame.time.Clock()

# Define all Variables
ball_pos_x = 40
ball_pos_y = 30
BALL_DIAMETER = 20

movement_x = 4
movement_y = 4

player1_x = 20
player1_y = 20
player1_movement = 0

player2_x = WINDOW_WIDTH - (2 * 20)
player2_y = 20
player2_movement = 0

paddle_height = 150
ball_bounces = 0

game_paused = False

# Main Loop
while game_active:
    # Get Player interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            game_active = False
            print("Player clicked quit button")
        if event.type == pygame.KEYDOWN:
            print("Player pressed a key")

            # Restart
            if event.key == pygame.K_r:
                ball_pos_x = 40
                ball_pos_y = 30
                movement_x = 4
                movement_y = 4
                player1_x = 20
                player1_y = 20
                player1_movement = 0
                player2_x = WINDOW_WIDTH - (2 * 20)
                player2_y = 20
                player2_movement = 0
                paddle_height = 150
                ball_bounces = 0

            # Pause
            if event.key == pygame.K_p:
                print("Pause game")
                if game_paused == True:
                    game_paused = False
                    pygame.mixer.music.unpause()
                    movement_x = pause_movement_x
                    movement_y = pause_movement_y
                else:
                    game_paused = True
                    pygame.mixer.music.pause()
                    pause_movement_x = movement_x
                    pause_movement_y = movement_y
                    movement_x = 0
                    movement_y = 0

            # P2 Interaction, KEYDOWN
            if event.key == pygame.K_UP:
                print("Player 2 pressed up arrow")
                player2_movement = -6
            elif event.key == pygame.K_DOWN:
                print("Player 2 pressed down arrow")
                player2_movement = 6

            # P1 Interaction, KEYDOWN
            elif event.key == pygame.K_w:
                print("Player 1 pressed w for up")
                player1_movement = -6
            elif event.key == pygame.K_s:
                print("Player 1 pressed s for down")
                player1_movement = 6

        if event.type == pygame.KEYUP:
            print("Player released a key")
            # P1 Interaction, KEY UP
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                print("Player 2 stops moving")
                player2_movement = 0
            # P2 Interaction, KEY UP
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                print("Player 1 stops moving")
                player1_movement = 0

    # P1 Movement
    if player1_movement != 0:
        player1_y += player1_movement
    if player1_y < 0:
        player1_y = 0
    if player1_y > WINDOW_HEIGHT - paddle_height:
        player1_y = WINDOW_HEIGHT - paddle_height

    # P2 Movement
    if player2_movement != 0:
        player2_y += player2_movement
    if player2_y < 0:
        player2_y = 0
    if player2_y > WINDOW_HEIGHT - paddle_height:
        player2_y = WINDOW_HEIGHT - paddle_height

    screen.fill(BLACK)

    # Draw Figures
    ball = pygame.draw.ellipse(screen, WHITE, [ball_pos_x, ball_pos_y, BALL_DIAMETER, BALL_DIAMETER])
    player1 = pygame.draw.rect(screen, WHITE, [player1_x, player1_y, 20, paddle_height])
    player2 = pygame.draw.rect(screen, WHITE, [player2_x, player2_y, 20, paddle_height])

    # Ball Movement
    ball_pos_x += movement_x
    ball_pos_y += movement_y

    # Ball bounce Y
    if ball_pos_y > WINDOW_HEIGHT - BALL_DIAMETER or ball_pos_y < 0:
        movement_y = movement_y * -1

    # Ball bounce X
    if ball_pos_x > WINDOW_WIDTH - BALL_DIAMETER or ball_pos_x < 0:
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Lost, r to restart: {ball_bounces}", True, RED)
        screen.blit(text, [WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3])

    # Collision P1 w Ball
    if player1.colliderect(ball):
        print("Collision P1")
        pygame.mixer.Sound.play(hit_sound)
        movement_x = movement_x * -1
        ball_pos_x = 40
        ball_bounces += 1
        paddle_height = max(paddle_height - 5, 70)

    # Collision P2 w Ball
    if player2.colliderect(ball):
        print("Collision P2")
        pygame.mixer.Sound.play(hit_sound)
        movement_x = movement_x * -1
        ball_pos_x = 570
        ball_bounces += 1
        paddle_height = max(paddle_height - 5, 70)

    output_text = "Ball bounces: " + str(ball_bounces)
    font = pygame.font.SysFont(None, 40)
    text = font.render(output_text, True, RED)
    screen.blit(text, [WINDOW_WIDTH / 3, 10])

    # Ball speed increasement
    if movement_x > 0:
        movement_x += 0.001
    else:
        movement_x -= 0.001

    if movement_y > 0:
        movement_y += 0.001
    else:
        movement_y -= 0.001

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
